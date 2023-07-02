from user_state import AgentState
from aiogram import Router, F

import asyncio
import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from aiogram.fsm.state import State, StatesGroup

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from aiogram.filters.command import Command

from search import search
from match_engine import find_match
import emoji

from aiogram.filters.callback_data import CallbackData


router = Router()


class RatesCallbackFactory(CallbackData, prefix="rate"):
    liked: bool
    subj_id: int
    obj_id: int


def get_match_command_keyboard() -> ReplyKeyboardMarkup:
    buttons = [[types.KeyboardButton(text="match")]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)


def get_match_keyboard(subj_id: int, obj_id: int) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
            text=emoji.LIKE,
            callback_data=RatesCallbackFactory(
                liked=True,
                subj_id=subj_id,
                obj_id=obj_id,
                )
            )

    builder.button(
            text=emoji.DISLIKE,
            callback_data=RatesCallbackFactory(
                liked=False,
                subj_id=subj_id,
                obj_id=obj_id,
                )
            )

    builder.adjust(2)

    return builder.as_markup()


@router.message(
        Text("match"),
        AgentState.registered
)
async def process_match(
        message: types.Message,
        state: FSMContext,
        agents
    ):
    user_id = message.from_user.id
    agent = agents[user_id]

    companion = find_match(agent, agents.values())

    if companion is None:
        await message.reply(
                text="На данный момент подходящих партнеров не найдено.",
                reply_markup=get_match_command_keyboard())
        return

    text = (
            f"{companion.name}, {companion.age}\n"
            f"{companion.about_yourself}")

    await message.answer_photo(
        companion.picture,
        caption=text,
        reply_markup=get_match_keyboard(user_id, companion.user_id))

    await state.set_state(AgentState.rates)


@router.message(
        Text("match"),
        AgentState.rates
        )
async def process_match(message: types.Message, agents):
    await message.reply("Сначала поставьте оценку предыдущему кандидату")


@router.callback_query(
        RatesCallbackFactory.filter(),
        AgentState.rates
        )
async def process_rate(
        callback: types.CallbackQuery,
        callback_data: RatesCallbackFactory,
        state: FSMContext,
        bot: Bot,
        agents
        ):
    subj_id = callback_data.subj_id
    obj_id = callback_data.obj_id

    subj = agents[subj_id]
    obj = agents[obj_id]

    if callback_data.liked:
        target_set = subj.liked_ids
        target_text = emoji.LIKE
    else:
        target_set = subj.disliked_ids
        target_text = emoji.DISLIKE

    target_set.add(obj_id)

    buttons = [
            [
                types.InlineKeyboardButton(
                    text=target_text,
                    callback_data=f"already_rated"
                    )
                ]
            ]

    await callback.message.edit_reply_markup(
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons))

    if (callback_data.liked
        and subj_id in obj.liked_ids
        ):
        reply_text = "🔥У вас взаимная симпатия с @{}🔥"
        await bot.send_message(obj_id, text=reply_text.format(subj.username))
        await bot.send_message(subj_id, text=reply_text.format(obj.username))

    await callback.answer()
    await state.set_state(AgentState.registered)

    await callback.message.answer(
            text="Оценка учтена",
            reply_markup=get_match_command_keyboard())

@router.callback_query(Text("already_rated"))
async def process_already_rates(
        callback: types.CallbackQuery,
        agents
        ):
    await callback.answer(text="Вы уже оценили этого человека")
