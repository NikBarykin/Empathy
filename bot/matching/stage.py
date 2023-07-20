from stage import Stage
from command_start import get_id

from matching.match import get_next_match
from matching.callback_rated import process_callback_rated, process_callback_already_rated
from matching.rating_callback_factory import RatingCallbackFactory

from aiogram import Router
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text


class MatchStage(Stage):
    state = State()
    name: str = "match"

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        await get_next_match(Stage.bot, await get_id(state), Stage.async_session)

async def process_no_partner_yet(
    bot: Bot,
    user_telegram_id: int,
    async_session: async_sessionmaker[AsyncSession],
) -> None:
    await User.put_in_waiting_pool(
        telegram_id=user_telegram_id, async_session=async_session)

    await bot.send_message( user_telegram_id, text=("На данный момент подходящих партнеров не найдено. "
                  "Когда появятся подходящие варианты, мы обязательно тебе напишем!😉"),
            reply_markup=types.ReplyKeyboardRemove())


async def process_found_partner(
        bot: Bot,
        user_telegram_id: int,
        partner: User,
        ) -> None:

    text = (f"{partner.name}, {partner.age}\n"
            f"{partner.self_description}")

    await bot.send_photo(
            user_telegram_id,
            partner.photo,
            caption=text,
            reply_markup=get_inline_kb(user_telegram_id, partner.telegram_id),
            )


async def get_next_match(
    bot: Bot,
    user_telegram_id: int,
    async_session: async_sessionmaker[AsyncSession],
):
    partner = await find_match(user_telegram_id, async_session)

    if partner is None:
        await process_no_partner_yet(bot, user_telegram_id, async_session)
    else:
        await process_found_partner(bot, user_telegram_id, partner)

    @staticmethod
    def register(router: Router) -> None:
        router.callback_query.register(
            process_callback_rated,
            RatingCallbackFactory.filter(),
            MatchStage.state,
        )

        router.callback_query.register(
            process_callback_already_rated,
            Text("already_rated"),
            MatchStage.state,
        )
