"""Main matchings stage in bot"""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from db.user import User
from db.rating import Rating

from utils.logger import create_logger
from utils.id import get_id

from engine.search import find_partner_for
# TODO:
# from engine.score import get_relationship_score
from engine.rating import submit_rating, check_mutual_sympathy
from engine.user import get_user_by_id

from stages.stage import Stage, go_stage
from stages.regular_workflow.profile.send import send_profile
from stages.regular_workflow.profile import ProfileStage

from .constants import PARTNERS_NOT_FOUND_TEXT

from .keyboard import get_query_kb, get_rated_kb
from .rating_callback_factory import RatingCallbackFactory
from .logic import send_partner, check_and_process_mutual_sympathy
from .waiting_pool import remove_from_waiting_pool, put_in_waiting_pool


class MatchStage(Stage):
    name: str = "Match-stage"
    __main_state = State(state=name)
    __prepare_state = State(state="prepare_" + name)
    __rating_state = State(state="rating_" + name)
    __logger = create_logger(name)

    @staticmethod
    async def send_partner(actor_id: int, partner: User):
        kb = await get_query_kb(
            actor_id=actor_id,
            target_id=partner.id,
            # TODO:
            partner_score=1,
        )
        return await send_profile(
            chat_id=actor_id,
            user=partner,
            reply_markup=kb,
        )

    @staticmethod
    async def prepare(state: FSMContext):
        await state.set_state(MatchStage.__prepare_state)

        actor_id: int = await get_id(state)

        target: User | None = await find_partner_for(actor_id)

        if target is None:
            MatchStage.__logger.info(
                "Didn't find a partner for %s", actor_id)

            await put_in_waiting_pool(
                actor_id, logger=MatchStage.__logger)

            result = await Stage.bot.send_message(
                actor_id,
                text=PARTNERS_NOT_FOUND_TEXT
            )

        else:
            MatchStage.__logger.info(
                "Found a partner %s for %s",
                target,
                actor_id,
            )

            await remove_from_waiting_pool(
                actor_id, logger=MatchStage.__logger)

            result = await send_partner(actor_id=actor_id, partner=target)

        await state.set_state(MatchStage.__main_state)

        return result

    @staticmethod
    async def process_rating(
        callback: CallbackQuery,
        callback_data: RatingCallbackFactory,
        state: FSMContext,
    ) -> None:
        """Process when one user rated other user"""
        await state.set_state(MatchStage.__rating_state)

        await Stage.bot.edit_reply_markup(
            reply_markup=get_rated_kb(callback_data.liked),
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
    async def process_go_profile(_: Message, state: FSMContext):
        """Process go to profile-stage"""
        return await go_stage(
            departure=MatchStage,
            destination=ProfileStage,
            state=state,
        )

    @staticmethod
    def register(router: Router) -> None:
        router.callback_query.register(
            MatchStage.process_rating,
            RatingCallbackFactory.filter(),
            MatchStage.__main_state,
        )

        router.message.register(
            MatchStage.process_go_profile,
            # F.text==f"/{ProfileStage.name}",
            Command(ProfileStage.name),
            MatchStage.__main_state,
        )
