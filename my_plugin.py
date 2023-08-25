from mad_hatter.decorators import tool, hook
from pydantic import BaseModel
from datetime import datetime, date


class MySettings(BaseModel):
    required_int: int
    optional_int: int = 69
    required_str: str
    optional_str: str = "meow"
    required_date: date
    optional_date: date = 1679616000


@hook
def plugin_settings_schema():
    return MySettings.schema()


@tool
def get_the_day(tool_input, bot):
    """Get the day of the week. Input is always None."""

    dt = datetime.now()

    return dt.strftime('%A')


@hook
def before_bot_sends_message(message, bot):
    prompt = f'Rephrase the following sentence in a grumpy way: {message["content"]}'
    message["content"] = bot.llm(prompt)

    return message
