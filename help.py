from aiogram import Router, F
import asyncio
import logging
import aiogram.utils.markdown as md
from aiogram import types, F
from aiogram.filters import Text
from aiogram.filters.command import Command

from agent import Agent

router = Router()

@router.message(Command("help"))
async def process_help(message: types.Message):
    message.reply("Not implemented yet")
