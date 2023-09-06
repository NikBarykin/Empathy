"""Main matchings stage in bot"""
from aiogram import Router
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.exceptions import TelegramBadRequest
from aiogram.methods import SendMessage, EditMessageReplyMarkup

from database.rating import Rating

from utils.logger import create_logger
from utils.id import get_id
from utils.keyboard import remove_reply_keyboard
from utils.execute_method import execute_method
from utils.order import make_stage_jumper

from engine.search import find_partner_for
# TODO:
# from engine.score import get_relationship_score
from engine.rating import submit_rating

from stage import Stage
from user_stages.profile import ProfileStage

from .constants import PARTNERS_NOT_FOUND_TEXT

from .keyboard import get_rated_kb
from .callback_factory import RatingCallbackFactory
from .logic import send_partner, check_and_process_mutual_sympathy
from .waiting_pool import remove_from_waiting_pool, put_in_waiting_pool


class MatchStage(Stage):
    """The main stage where user rates (like/dislike) potential partners"""
    name: str = "Match-stage"
    __main_state = State(state=name)
    __prepare_state = State(state="prepare_" + name)
    __rating_state = State(state="rating_" + name)
    __logger = create_logger(name)

    @staticmethod
    async def __process_no_partner(actor_id: int, state: FSMContext) -> Message | None:
        """Process a situation when there is no partner for actor_id"""
        MatchStage.__logger.info(
            "Didn't find a partner for %s", actor_id)

        await put_in_waiting_pool(
            actor_id, logger=MatchStage.__logger)

        # TODO process error-situation (for example when user blocked bot)
        result: Message | None = await execute_method(
            SendMessage(
                chat_id=actor_id,
                text=PARTNERS_NOT_FOUND_TEXT,
                reply_markup=ReplyKeyboardRemove(),
            ),
            logger=MatchStage.__logger,
        )

        await state.set_state(MatchStage.__main_state)

        return result

    @staticmethod
    async def __process_found_partner(
        actor_id: int,
        target_id: int,
        state: FSMContext,
    ) -> Message:
        """Found a partner 'target_id' for 'actor_id'"""
        MatchStage.__logger.info(
            "Found a partner %s for %s",
            target_id,
            actor_id,
        )

        await remove_from_waiting_pool(
            actor_id, logger=MatchStage.__logger)

        result: Message | None = await send_partner(
            actor_id=actor_id,
            partner_id=target_id,
            logger=MatchStage.__logger,
        )

        if result is None:
            # something wend wrong
            MatchStage.__logger.warning(
                "Partner %s was ignored, because his photo expired or something else went wrong: %s", target_id, e)
            await submit_rating(
                Rating(
                    liked=False,
                    actor_id=actor_id,
                    target_id=target_id,
                ),
                logger=MatchStage.__logger,
            )
            return await MatchStage.prepare(state)

        await remove_reply_keyboard(chat_id=actor_id)

        await state.set_state(MatchStage.__main_state)

        return result

    @staticmethod
    async def prepare(state: FSMContext):
        """Search for a partner"""
        await state.set_state(MatchStage.__prepare_state)

        actor_id: int = await get_id(state)

        target_id: int | None = await find_partner_for(actor_id)

        if target_id is None:
            return await MatchStage.__process_no_partner(actor_id, state)
        return await MatchStage.__process_found_partner(
            actor_id, target_id, state)

    @staticmethod
    async def process_rating(
        callback: CallbackQuery,
        callback_data: RatingCallbackFactory,
        state: FSMContext,
    ) -> Message:
        """Process when one user rated other user"""
        await state.set_state(MatchStage.__rating_state)

        await execute_method(
            EditMessageReplyMarkup(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                reply_markup=get_rated_kb(callback_data.liked),
            ),
            logger=MatchStage.__logger,
        )

        new_rating = Rating(
            liked=callback_data.liked,
            actor_id=callback_data.actor_id,
            target_id=callback_data.target_id,
        )

        await submit_rating(new_rating, logger=MatchStage.__logger)

        # check if there is a mutual sympathy
        await check_and_process_mutual_sympathy(
            new_rating.actor_id,
            new_rating.target_id,
            logger=MatchStage.__logger,
        )

        await callback.answer()
        await MatchStage.prepare(state)

    @staticmethod
    def register(router: Router) -> None:
        router.callback_query.register(
            MatchStage.process_rating,
            RatingCallbackFactory.filter(),
            MatchStage.__main_state,
        )

        router.message.register(
            make_stage_jumper(target_stage=ProfileStage),
            Command(ProfileStage.name),
            MatchStage.__main_state,
        )
