# pip install python-dotenv
from dotenv import load_dotenv
import os


load_dotenv()
# use a .env file to save your API keys and use like
# api_key = os.environ["GROQ_API_KEY"]


def synthesize_audio(script : str,voice_code : int) -> str:
    """
    TODO
    parameter : 
    script (str) : entire script to synthesize
    voice_code (int) : [0,1,2,3,4]

    Use GROQ apis to synthesize audio for the given script.
    use these voices according to voice code:
    0 : Quinn
    1 : Nia
    2 : Chip
    3 : Arista
    4 : Angelo

    Find the actual api paramter from the docs.
    save the wav file in a tmp folder inside utils folder.

    TIP : keep the len(script) < 20-30 for testing or you will exhaust you api credits.

    return:
    str : File path of the saved synthesis
    """
    pass
