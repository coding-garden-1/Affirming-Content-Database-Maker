from gtts import gTTS
from pydub import AudioSegment
import os

# Function to convert text to speech and save it to a file
def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

# Function to add silence
def add_silence(audio_segment, duration_ms):
    silence = AudioSegment.silent(duration=duration_ms)
    return audio_segment + silence

# Load background music
bgm = AudioSegment.from_mp3("bgm.mp3")

# Read text file with sentences
with open("tape.txt", "r") as file:
    sentences = file.readlines()

# Create separate text files for each sentence
for i, sentence in enumerate(sentences):
    text_filename = f"text_{i}.txt"
    with open(text_filename, "w") as text_file:
        text_file.write(sentence.strip())

# List to hold file names of generated speech segments
speech_filenames = []

# Convert each sentence to speech, save it to a file, and adjust volume
for i in range(len(sentences)):
    text_filename = f"text_{i}.txt"
    speech_filename = f"speech_{i}.mp3"
    
    # Convert text to speech and save it to a file
    text = open(text_filename, "r").read()
    text_to_speech(text, speech_filename)
    
    # Adjust volume of speech segment
    speech_segment = AudioSegment.from_mp3(speech_filename) - 3
    
    # Save the adjusted speech segment to a file
    adjusted_speech_filename = f"adjusted_speech_{i}.mp3"
    speech_segment.export(adjusted_speech_filename, format="mp3")
    
    # Add the filename to the list
    speech_filenames.append(adjusted_speech_filename)

# List to hold each speech segment with 15 seconds of silence
final_segments_with_silence = []

# Add each speech segment to the final audio with 15 seconds of silence between them
for speech_filename in speech_filenames:
    # Load the speech segment
    speech_segment = AudioSegment.from_mp3(speech_filename)
    
    # Add the speech segment to the list of final segments
    final_segments_with_silence.append(speech_segment)
    
    # Add 15 seconds of silence after each speech segment
    final_segments_with_silence.append(AudioSegment.silent(duration=15000))

# Concatenate all segments
final_audio = sum(final_segments_with_silence)

# Overlay with background music
final_audio_with_bgm = final_audio.overlay(bgm)

# Save final audio as "tape_audio.mp3"
final_audio_with_bgm.export("tape_audio.mp3", format="mp3")

# Clean up temporary files
for filename in speech_filenames:
    if os.path.exists(filename):
        os.remove(filename)

for i in range(len(sentences)):
    text_filename = f"text_{i}.txt"
    if os.path.exists(text_filename):
        os.remove(text_filename)
    
    adjusted_speech_filename = f"adjusted_speech_{i}.mp3"
    if os.path.exists(adjusted_speech_filename):
        os.remove(adjusted_speech_filename)
    
    speech_filename = f"speech_{i}.mp3"
    if os.path.exists(speech_filename):
        os.remove(speech_filename)
