import os
import time
import math
import tiktoken
from pydub import AudioSegment
from dotenv import load_dotenv
from groq import Groq


load_dotenv()
API_KEY = os.environ["GROQ_API_KEY"]


VOICE_MAP = {
    0: "Quinn-PlayAI",
    1: "Nia-PlayAI",
    2: "Chip-PlayAI",
    3: "Arista-PlayAI",
    4: "Angelo-PlayAI"
}

OUTPUT_DIR = os.path.join("utils", "tmp")
os.makedirs(OUTPUT_DIR, exist_ok=True)


ENCODING = tiktoken.get_encoding("cl100k_base")
MAX_TOKENS_PER_CHUNK = 600


def synthesize_audio(script: str, voice_code: int) -> str:
    

    if voice_code not in VOICE_MAP:
        raise ValueError("Invalid voice code. Use an integer from 0 to 4.")

    voice = VOICE_MAP[voice_code]
    client = Groq(api_key=API_KEY)

    
    tokens = ENCODING.encode(script)
    token_chunks = [tokens[i:i + MAX_TOKENS_PER_CHUNK] for i in range(0, len(tokens), MAX_TOKENS_PER_CHUNK)]
    text_chunks = [ENCODING.decode(chunk) for chunk in token_chunks]

    file_paths = []

    for i, chunk_text in enumerate(text_chunks):
        print(f"🎤 Synthesizing chunk {i+1}/{len(text_chunks)}...")
        try:
            response = client.audio.speech.create(
                model="playai-tts",
                voice=voice,
                input=chunk_text,
                response_format="wav"
            )
            chunk_path = os.path.join(OUTPUT_DIR, f"chunk_{i+1}.wav")
            response.write_to_file(chunk_path)
            file_paths.append(chunk_path)
        except Exception as e:
            print(f"❌ Error generating audio for chunk {i+1}: {e}")
            break

        time.sleep(1.5) 

    if not file_paths:
        raise RuntimeError("No audio chunks were generated.")

    
    print("🔗 Merging chunks...")
    final_audio = AudioSegment.empty()
    for file in file_paths:
        final_audio += AudioSegment.from_wav(file)

    final_output = os.path.join(OUTPUT_DIR, "speech_final.wav")
    final_audio.export(final_output, format="wav")

    print(f"✅ Speech synthesis complete: {final_output}")
    return final_output