from stage import Stage
from command_start import get_id

from db.rating import Rating
from db.user import User
from db.match import check_liked, find_match, get_user_by_telegram_id


from matching.keyboards import get_inline_kb
from matching.rating_callback_factory import RatingCallbackFactory

from aiogram import Router, types
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder

from constants import LIKE_EMOJI, DISLIKE_EMOJI

from sqlalchemy.ext.asyncio import AsyncSession


def get_already_rated_kb(
        liked: bool
        ) -> types.InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
            text=(LIKE_EMOJI if liked else DISLIKE_EMOJI),
            callback_data="already_rated",
            )
    return keyboard.as_markup()


async def insert_rating(
        liked: bool,
        subj: User,
        obj: User,
        session: AsyncSession,
        ) -> None:
    async with session.begin():
        session.add(
                Rating(
                    liked,
                    subj,
                    obj,
                    )
                )


class MatchStage(Stage):
    state = State()
    name: str = "match"

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        await MatchStage.get_next_match(await get_id(state))

    @staticmethod
    async def process_no_partner_yet(
        user_telegram_id: int,
    ) -> None:
        await User.put_in_waiting_pool(
            telegram_id=user_telegram_id, async_session=Stage.async_session)

        await Stage.bot.send_message( user_telegram_id, text=(
            "На данный момент партнеров не найдено. "
            "Когда появятся подходящие варианты, мы обязательно тебе напишем!😉"),
                                     reply_markup=types.ReplyKeyboardRemove())

    @staticmethod
    async def process_found_partner(
            user_telegram_id: int,
            partner: User,
            ) -> None:

        text = (f"{partner.name}, {partner.age}\n"
                f"{partner.self_description}")

        await Stage.bot.send_photo(
                user_telegram_id,
                partner.photo,
                caption=text,
                reply_markup=get_inline_kb(
                    user_telegram_id, partner.telegram_id),
                )

    @staticmethod
    async def get_next_match(
        user_telegram_id: int,
    ):
        partner = await find_match(user_telegram_id, Stage.async_session)

        if partner is None:
            await MatchStage.process_no_partner_yet(user_telegram_id)
        else:
            await MatchStage.process_found_partner(user_telegram_id, partner)

    @staticmethod
    async def process_callback_rated(
        callback: types.CallbackQuery,
        callback_data: RatingCallbackFactory,
    ) -> None:
        async with Stage.async_session() as session:
            subj = await get_user_by_telegram_id(
                    callback_data.subj_telegram_id,
                    session)

            obj = await get_user_by_telegram_id(
                    callback_data.obj_telegram_id,
                    session)

            liked: bool = callback_data.liked

            await insert_rating(
                    liked,
                    subj,
                    obj,
                    session,
                    )

            await callback.message.edit_reply_markup(
                    reply_markup=get_already_rated_kb(liked),
                    )

            # check for mutual sympathy
            liked_back: bool = await check_liked(obj, subj, session)
            if liked and liked_back:

                reply_text = "🔥У вас взаимная симпатия с @{}🔥"

                await Stage.bot.send_message(
                        obj.telegram_id,
                        text=reply_text.format(subj.telegram_handle),
                        )

                await Stage.bot.send_message(
                        subj.telegram_id,
                        text=reply_text.format(obj.telegram_handle),
                        )

        await callback.answer()

        await MatchStage.get_next_match(
                user_telegram_id=callback_data.subj_telegram_id,
                )

    @staticmethod
    async def process_callback_already_rated(
            callback: types.CallbackQuery,
            ):
        await callback.answer(text="Вы уже оценили этого человека")

    @staticmethod
    def register(router: Router) -> None:
        router.callback_query.register(
            MatchStage.process_callback_rated,
            RatingCallbackFactory.filter(),
            MatchStage.state,
        )

        router.callback_query.register(
            MatchStage.process_callback_already_rated,
            Text("already_rated"),
            MatchStage.state,
        )
