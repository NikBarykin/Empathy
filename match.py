from user_state import AgentState
from aiogram import Router, F

import asyncio
import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from aiogram.fsm.state import State, StatesGroup

from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.filters.command import Command

from search import search
from match_engine import find_match
import emoji

from aiogram.filters.callback_data import CallbackData


router = Router()

class RatesCallbackFactory(CallbackData, prefix="rate"):
    like: bool
    subj_id: int
    obj_id: int

def get_match_keyboard(subj_id: int, obj_id: int) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
            text=emoji.LIKE,
            callback_data=RatesCallbackFactory(
                like=True,
                subj_id=subj_id,
                obj_id=obj_id,
                )
            )

    builder.button(
            text=emoji.DISLIKE,
            callback_data=RatesCallbackFactory(
                like=False,
                subj_id=subj_id,
                obj_id=obj_id,
                )
            )

    builder.adjust(2)

    return builder.as_markup()


@router.message(
        Command("match"),
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
        message.reply("There is no match yet:(")
        return

    text = f"{companion.user_name}, {companion.age}"

    await message.answer_photo(
        companion.picture,
        caption=text,
        reply_markup=get_match_keyboard(user_id, companion.user_id))

    await state.set_state(AgentState.rates)


@router.message(
        Command("match"),
        AgentState.rates
        )
async def process_match(message: types.Message, agents):
    await message.reply("Before finding the next person you have to rate previous one")


@router.callback_query(RatesCallbackFactory.filter())
async def process_rate(
        callback: types.CallbackQuery,
        callback_data: RatesCallbackFactory,
        state: FSMContext,
        agents
        ):
    subj_id = callback_data.subj_id
    obj_id = callback_data.obj_id

    subj = agents[subj_id]

    if callback_data.like:
        target_set = subj.like_ids
        target_text = emoji.LIKE
    else:
        target_set = subj.dislike_ids
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

    if (callback_data.like
        and subj_id in agents[obj_id].like_ids
        ):
        await callback.message.reply(text="There is a match!")

    await callback.answer()
    await state.set_state(AgentState.registered)

@router.callback_query(Text("already_rated"))
async def process_already_rates(
        callback: types.CallbackQuery,
        agents
        ):
    await callback.answer(text="You have already rated this person")
