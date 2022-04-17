import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.silence import detect_nonsilent

r = sr.Recognizer()

def make_three_number(number):
    number = str(number)
    while len(number) < 3:
        number += "0"
    return number

def make_two_number(number):
    number = str(number)
    while len(number) < 2:
        number = "0" + number
    return number

def nonsilent_object_to_srt_time_string(array):
    start,finish = array[0],array[1]
    startDict = {}
    finishDict = {}

    startDict["Milisecond"] = make_three_number(start%1000)
    start = int(start/1000)
    startDict["Second"] = make_two_number(start%60)
    startDict["Minute"] = make_two_number(int(start/60)%60)
    startDict["Hour"] = make_two_number(int(start/60/60))

    finishDict["Milisecond"] = make_three_number(finish%1000)
    finish = int(finish/1000)
    finishDict["Second"] = make_two_number(finish%60)
    finishDict["Minute"] = make_two_number(int(finish/60)%60)
    finishDict["Hour"] = make_two_number(int(finish/60/60))

    time_string = f'{startDict["Hour"]}:{startDict["Minute"]}:{startDict["Second"]},{startDict["Milisecond"]} --> '
    time_string += f'{finishDict["Hour"]}:{finishDict["Minute"]}:{finishDict["Second"]},{finishDict["Milisecond"]}'
    return time_string

def get_large_audio_transcription(path,lang):
    print("Audio Translating Started")
    path += ".wav"

    sound = AudioSegment.from_wav(path)
    # sound += 20
    chunks = split_on_silence(sound,
        min_silence_len = 450,
        silence_thresh = sound.dBFS-14,
        keep_silence=450,
    )
    chunks_details = detect_nonsilent(sound,
        min_silence_len = 450,
        silence_thresh = sound.dBFS-14,
    )
    
    srt_file_content = []
    print_counter = 1
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened,language=lang)
            except sr.UnknownValueError as e:
                pass
            else:
                text = f"{text.capitalize()}. "
                srt_file_content.append(f"{print_counter}")
                srt_file_content.append(nonsilent_object_to_srt_time_string(chunks_details[i-1]))
                srt_file_content.append(text)
                srt_file_content.append("")
                print(f"{i}/{len(chunks)}")
                print_counter += 1 


    for i in range(len(chunks)):
        file_path = os.path.join(folder_name, f"chunk{i+1}.wav")
        if os.path.exists(file_path):
            os.remove(file_path)
    os.rmdir(folder_name)
    if srt_file_content[len(srt_file_content)-1] == "\n":
        del srt_file_content[len(srt_file_content)-1]
    print("Audio Translating Finished")
    return srt_file_content