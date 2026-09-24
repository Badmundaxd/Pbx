from pyrogram import Client, filters
from pyrogram.types import Message
from pydub import AudioSegment
import os
import random
import time
from . import *

@on_message("test", enable_log=True)
@error_logger
async def test_command(client: Client, message: Message):
    await Pbxbot.edit(message, "Testing...")
    # Yeh line error dega kyunki koi variable nahi hai
    print(undefined_variable)  # Intentional error for testing
