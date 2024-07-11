from transformers import AutoProcessor, MusicgenForConditionalGeneration, AutoTokenizer
import torch
import pyaudio
import numpy as np
import os
import random
import wave
from pydub import AudioSegment

# Path to the pre-trained model
MODEL_PATH = "facebook/musicgen-small"

# Initialize processor, model, and tokenizer from pre-trained versions
processor = AutoProcessor.from_pretrained(MODEL_PATH)
model = MusicgenForConditionalGeneration.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

full_audio_data1 = []
full_audio_data = []
songcounter = 0

def print_shapes(data_list):
    for idx, chunk in enumerate(data_list):
        print(f"Shape of chunk {idx}: {chunk.shape}")

def generate_music(audio_chunk, text_inputs, songcountergoal, generated_prompt):
    global songcounter

    while songcounter < songcountergoal:
        audio_inputs = processor(audio=audio_chunk[0], sampling_rate=32000, return_tensors="pt")
        inputs = {**audio_inputs, **text_inputs}

        # Generate music based on the audio prompt and text prompt and get the audio values
        print("generating music from model")
        
        outputs = model.generate(**inputs, do_sample=True, guidance_scale=3, max_new_tokens=chunk_length)
        print(outputs.shape)
        audio_chunk = outputs[0].cpu().numpy()

        # Normalize the chunk
        audio_chunk = audio_chunk.astype(np.float32)
        audio_chunk /= np.max(np.abs(audio_chunk))

        songcounter += 1
        print(songcounter)
        print("added chunk")

        # Check if audio_chunk is too long
        if audio_chunk.shape[1] >= 160000:
            print("audio chunk is too long")
            # Process the first 640000 tokens separately
            first_chunk = audio_chunk[:, :80000]
            # Normalize the chunk
            first_chunk = first_chunk.astype(np.float32)
            first_chunk /= np.max(np.abs(first_chunk))
            # Send the first chunk for processing
            resizeandplay_audio(first_chunk, songcounter, songcountergoal, generated_prompt)

            # Use the most recent 640000 tokens for further generation
            audio_chunk = audio_chunk[:, -80000:]

        else:
            # Normalize the chunk
            audio_chunk = audio_chunk.astype(np.float32)
            audio_chunk /= np.max(np.abs(audio_chunk))

    return resizeandplay_audio(audio_chunk, songcounter, songcountergoal, generated_prompt)

import numpy as np

# ... (other code)

def resizeandplay_audio(audio_chunk, songcounter, songcountergoal, generated_prompt):
    global full_audio_data
    

    if songcounter != 0:
        full_audio_data.append(audio_chunk)
        print_shapes(full_audio_data)

    if songcounter == songcountergoal:
        # Check if all audio chunks have the same dimensions
        if all(chunk.shape == full_audio_data[0].shape for chunk in full_audio_data):
            # Reshape each chunk to (1, 1, n) and then concatenate along the time axis
            audio_data = np.concatenate([chunk.reshape(1, 1, -1) for chunk in full_audio_data], axis=2)
            print(audio_data.shape)
            return playmusic(audio_data, generated_prompt, songcounter)
        else:
            print("Not all audio chunks have the same dimensions. Skipping concatenation.")
            return



def playmusic(audio_data, generated_prompt, songcounter):
    # Parameters for pyaudio
    print(f"songcounter" + str(songcounter))
    songcounter = 0
    print(f"Playing music for prompt: {generated_prompt}")
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 44100  # Adjust this value if needed

    wav_filename = "temp_audio.wav"
    mp3_filename = f"music_prompt.mp3"

    audio_data_int16 = np.int16(audio_data * 32767)

    # Start pyaudio stream and play audio
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
    stream.write(audio_data.tobytes())

    with wave.open(wav_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(audio_data_int16.tobytes())


    stream.stop_stream()
    stream.close()
    p.terminate()

    audio = AudioSegment.from_wav(wav_filename)
    audio.export(mp3_filename, format="mp3", bitrate="320k", parameters=["-ar", "44100"])

    # Optionally, remove the temporary WAV file
    os.remove(wav_filename)

    print(f"Music saved as {mp3_filename}")

if __name__ == "__main__":
    num_prompts = 3  # Number of prompts to generate

    for i in range(num_prompts):
        songcounter = 0  # Reset songcounter at the start of each iteration
        
        prompt_path = os.path.join(os.path.dirname(__file__), f"response_{i + 1}.txt")
        with open(prompt_path, "r") as f:
            generated_prompt = f.read()

        # Process the input text prompt from the generated prompt
        text_inputs = processor(
            text=["Jazz music" +  " " + generated_prompt],
            padding=True,
            return_tensors="pt",
        )

        # Decide on chunk size:
        chunk_length = 128  # Adjust based on what works

        songcountergoal = random.randint(5, 7)

        for _ in range(songcountergoal):
            outputs = model.generate(**text_inputs, do_sample=True, guidance_scale=3, max_new_tokens=chunk_length)
            print(outputs.shape)
            print("generating")

            audio_chunk = outputs[0].cpu().numpy()
            
            print(f"Prompt {i + 1}: {generated_prompt}")
            print(audio_chunk.shape[1])

            generate_music(audio_chunk, text_inputs, songcountergoal, generated_prompt)


