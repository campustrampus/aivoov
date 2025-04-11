import base64
import io
import json
import os
import pydub
import requests
import string

from multiprocessing.dummy import Pool as ThreadPool

AUDIO_DIR = f'{os.getcwd()}/audio'
TIMESTAMP_DIR = f'{os.getcwd()}/timestamps'
FILE_NAME = f'{os.getcwd()}/resources/debby-2.txt'
MALE_VOICE = 'd7c2b60e-185b-4447-902f-2283c4afa876' 
FEMALE_VOICE = 'f2bc131c-436b-4581-97d0-28fb9e6e35e2'
VOICE_SETTINGS = {
          'mercy': {'speed': 1, 'stability': .20, 'similarity_boost': .90, 'style': .15, 'use_speaker_boost': True}, 
          'mercy (inner)': {'speed': 1, 'stability': .20, 'similarity_boost': .90, 'style': .15, 'use_speaker_boost': True}, 
          'simon': {'speed': 0.9, 'stability': .25, 'similarity_boost': .70, 'style': .15, 'use_speaker_boost': True}, 
          'simon (inner)': {'speed': 0.9, 'stability': .25, 'similarity_boost': .70, 'style': .15, 'use_speaker_boost': True}, 
          'john': {'speed': 1.05, 'stability': .20, 'similarity_boost': .75, 'style': .50, 'use_speaker_boost': True}, 
          'john (inner)': {'speed': 1.05, 'stability': .20, 'similarity_boost': .75, 'style': .50, 'use_speaker_boost': True}, 
          'christopher': {'speed': 0.96, 'stability': .25, 'similarity_boost': .86, 'style': .75, 'use_speaker_boost': True}, 
          'christopher (inner)': {'speed': 0.96, 'stability': .25, 'similarity_boost': .86, 'style': .75, 'use_speaker_boost': True}, 
          'debby': {'speed': 1, 'stability': .30, 'similarity_boost': .75, 'style': .80, 'use_speaker_boost': True}, 
          'debby (inner)': {'speed': 1, 'stability': .30, 'similarity_boost': .75, 'style': .80, 'use_speaker_boost': True}, 
          'anna': {'speed': 1, 'stability': .25, 'similarity_boost': .80, 'style': .80, 'use_speaker_boost': True}, 
          'anna (inner)': {'speed': 1, 'stability': .25, 'similarity_boost': .80, 'style': .80, 'use_speaker_boost': True}, 
          'dr. kamau': {'speed': 1, 'stability': .25, 'similarity_boost': .17, 'style': .50, 'use_speaker_boost': True}, 
          'dr. atieno': {'speed': 1.1, 'stability': .25, 'similarity_boost': .80, 'style': .80, 'use_speaker_boost': True}, 
          'dr. mungai': {'speed': 1.15, 'stability': .20, 'similarity_boost': .80, 'style': .80, 'use_speaker_boost': True}, 
          'stephen': {'speed': 1, 'stability': .30, 'similarity_boost': .80, 'style': .80, 'use_speaker_boost': True}, 
          'jenny': {'speed': 0.9, 'stability': .20, 'similarity_boost': .75, 'style': .75, 'use_speaker_boost': True}, 
          'peter': {'speed': 1, 'stability': .25, 'similarity_boost': .80, 'style': .50, 'use_speaker_boost': True}, 
          "anna's mum": {'speed': 1, 'stability': .30, 'similarity_boost': .90, 'style': .90, 'use_speaker_boost': True}, 
          "simon's mum": {'speed': 1, 'stability': .25, 'similarity_boost': .80, 'style': .80, 'use_speaker_boost': True}, 
          "mercy's father": {'speed': 1, 'stability': .20, 'similarity_boost': .75, 'style': .70, 'use_speaker_boost': True}, 
          "debby's mum": {'speed': 1, 'stability': .25, 'similarity_boost': .80, 'style': .70, 'use_speaker_boost': True}, 
          "christopher's mother": {'speed': 1.05, 'stability': .30, 'similarity_boost': .75, 'style': .90, 'use_speaker_boost': True}, 
          "grandfather": {'speed': 1.1, 'stability': .25, 'similarity_boost': .75, 'style': .80, 'use_speaker_boost': True}, 
          'aunt julia': {'speed': 1, 'stability': .25, 'similarity_boost': .80, 'style': .80, 'use_speaker_boost': True}, 
          'sam': {'speed': 1, 'stability': .20, 'similarity_boost': .75, 'style': .85, 'use_speaker_boost': False}, 
          'james': {'speed': 1, 'stability': .25, 'similarity_boost': .65, 'style': .70, 'use_speaker_boost': False}, 
          'george': {'speed': 1.15, 'stability': .35, 'similarity_boost': .60, 'style': .60, 'use_speaker_boost': False}, 
          'erick': {'speed': 0.95, 'stability': .20, 'similarity_boost': .65, 'style': .70, 'use_speaker_boost': True}, 
          'maryam': {'speed': 1, 'stability': .20, 'similarity_boost': .90, 'style': .90, 'use_speaker_boost': True}, 
          'ben': {'speed': 1, 'stability': .30, 'similarity_boost': .75, 'style': .75, 'use_speaker_boost': True}, 
          'vivian': {'speed': 1, 'stability': .25, 'similarity_boost': .75, 'style': .80, 'use_speaker_boost': True}, 
          'faith': {'speed': 0.9, 'stability': .20, 'similarity_boost': .70, 'style': .60, 'use_speaker_boost': True}, 
          'violet': {'speed': 0.9, 'stability': .25, 'similarity_boost': .70, 'style': .60, 'use_speaker_boost': True}, 
          'adhiambo': {'speed': 1, 'stability': .25, 'similarity_boost': .80, 'style': .85, 'use_speaker_boost': True}, 
          'otis': {'speed': 1, 'stability': .30, 'similarity_boost': .75, 'style': .85, 'use_speaker_boost': True},  
          'auma': {'speed': 1, 'stability': .25, 'similarity_boost': .65, 'style': .80, 'use_speaker_boost': True},  
          'akinyi': {'speed': 1, 'stability': .30, 'similarity_boost': .75, 'style': .70, 'use_speaker_boost': True},  
          'joe': {'speed': 1, 'stability': .30, 'similarity_boost': .85, 'style': .85, 'use_speaker_boost': True}, 
          'kyalo': {'speed': 1, 'stability': .25, 'similarity_boost': 1.00, 'style': 1.00, 'use_speaker_boost': True}, 
          'alex': {'speed': 1, 'stability': .30, 'similarity_boost': .75, 'style': .75, 'use_speaker_boost': True}, 
          'cynthia': {'speed': 1, 'stability': .30, 'similarity_boost': .70, 'style': .70, 'use_speaker_boost': True}, 
          'omondi': {'speed': 1, 'stability': .30, 'similarity_boost': .60, 'style': .70, 'use_speaker_boost': True}, 
          'isaac': {'speed': 1, 'stability': .25, 'similarity_boost': .75, 'style': .50, 'use_speaker_boost': True}, 
          'paul': {'speed': 1, 'stability': .30, 'similarity_boost': .65, 'style': .70, 'use_speaker_boost': True}, 
          'catherine': {'speed': 1, 'stability': .25, 'similarity_boost': .80, 'style': .75, 'use_speaker_boost': True}, 
          'matthew': {'speed': 0.95, 'stability': .30, 'similarity_boost': .60, 'style': .60, 'use_speaker_boost': False}, 
          'brian': {'speed': 1, 'stability': .30, 'similarity_boost': .80, 'style': 1.00, 'use_speaker_boost': True}, 
          'mary': {'speed': 1.1, 'stability': .30, 'similarity_boost': .80, 'style': .80, 'use_speaker_boost': True}, 
          'ryan': {'speed': 1.1, 'stability': .30, 'similarity_boost': .75, 'style': .50, 'use_speaker_boost': True}, 
          'anthony': {'speed': 1, 'stability': .20, 'similarity_boost': .40, 'style': .90, 'use_speaker_boost': False}, 
          'william': {'speed': 1, 'stability': .25, 'similarity_boost': .80, 'style': .80, 'use_speaker_boost': True}, 
          'ms. muthoni': {'speed': 1, 'stability': .25, 'similarity_boost': .80, 'style': .80, 'use_speaker_boost': True}, 
          'mr. makori': {'speed': 1, 'stability': .35, 'similarity_boost': .75, 'style': .60, 'use_speaker_boost': True}, 
          'gasira': {'speed': 1, 'stability': .10, 'similarity_boost': .80, 'style': .90, 'use_speaker_boost': True}, 
          'thomas': {'speed': 1, 'stability': .30, 'similarity_boost': .40, 'style': .75, 'use_speaker_boost': True}, 
          'eddie': {'speed': 1, 'stability': .20, 'similarity_boost': .70, 'style': .80, 'use_speaker_boost': True}, 
        }
TOKEN = ""
VOICES = {}
SESSION = requests.Session()
SCENE_NAMES = set()

scenes_to_run_audio = [
]
class Act:
    def __init__(self, data):
        self.pre_scene_lines = []
        self.scenes = []
        self.raw_data = data
        self.has_generate_audio = False
        current_scene = None
        current_speaker = None
        for raw_line in data.split('\n'):
            # Enter into a new scene
            if raw_line.strip().startswith('=='):
              current_scene = Scene(name=raw_line.split('==')[1].strip(), lines=[])
              if current_scene.name in SCENE_NAMES:
                  print(f"ERROR DUPLICATE SCENE NAME {current_scene.name}")
              else:
                SCENE_NAMES.add(current_scene.name)
              if ' ' in raw_line.split('==')[1].strip():
                  print(f"Error space in scene name {current_scene.name}")
              self.scenes.append(current_scene)
              current_scene.raw_lines.append(raw_line)
              continue
            if not current_scene:
                self.pre_scene_lines.append(raw_line)
            else:
                current_scene.raw_lines.append(raw_line)
                if is_dialogue(raw_line, current_scene.name):
                    line = parse_dialogue_line(raw_line, current_speaker=current_speaker)
                    current_speaker = line.person
                    current_scene.lines.append(line)
                    if raw_line.strip().startswith('+ ['):
                        current_scene.has_choice_bug = True
                    if current_scene.name in scenes_to_run_audio:
                        current_scene.rerun_audio = True
                elif raw_line.strip().upper().startswith('#FADE_IN'):
                    current_scene.has_fade_in = True
                elif raw_line.strip().upper().startswith('#FADE_OUT'):
                    current_scene.has_fade_out = True
        
    def generate_ink_file(self):
        with open(FILE_NAME + '.ink', mode='w') as f:
            for raw_line in self.pre_scene_lines:
                if raw_line.strip().startswith('_________________________________________________________________________________'):
                    pass
                else:
                    f.write(raw_line.strip() + '\n')
            
            for scene in self.scenes:
                in_choice = False
                printed_fade_out = False
                choices = 0
                buffer = io.StringIO()
                current_time = -1
                current_dialogue_line = 0
                last_written_time = 0
                try:
                    for raw_line in scene.raw_lines:
                        # Scene title line
                        if not scene.lines:
                            f.write(raw_line.strip() + '\n')
                        elif raw_line.strip().startswith('=='):
                            f.write(raw_line.strip() + '\n')
                        elif is_dialogue(raw_line, scene.name):
                            in_time = False
                            if raw_line.strip().startswith('+[') or raw_line.strip().startswith('+ ['):
                                in_choice = True
                                buffer.write(raw_line + '\n')
                                choices += 1
                                current_dialogue_line += 1
                            elif in_choice:
                                print(f"ERROR, found dialogue after choice in {scene.name}")
                                pass
                            else:
                                if current_time -1:
                                    f.write('#TIME 0\n')
                                if scene.lines[current_dialogue_line].start_time > 0 and current_dialogue_line == 0:
                                    buffer.seek(0)
                                    f.write(buffer.read())
                                    buffer.seek(0)
                                    buffer.truncate(0)
                                    f.write(f'#TIME {round(scene.lines[current_dialogue_line].start_time, 2)}\n')
                                elif scene.lines[current_dialogue_line].start_time > 0:
                                    buffer.seek(0)
                                    f.write(buffer.read())
                                    buffer.seek(0)
                                    buffer.truncate(0)
                                    f.write(f'#TIME {round(scene.lines[current_dialogue_line].start_time, 2)}\n')
                                elif current_time == 0:
                                    buffer.seek(0)
                                    f.write(buffer.read())
                                    buffer.seek(0)
                                    buffer.truncate(0)
                                dialogue = raw_line.strip().split(':')
                                f.write(':'.join(dialogue[1:]).strip() + '\n\n')
                                current_time = round(scene.lines[current_dialogue_line].end_time, 2)
                                current_dialogue_line += 1
                                if current_dialogue_line == len(scene.lines):
                                    last_written_time = round(scene.lines[current_dialogue_line-1].end_time, 2)
                                    f.write(f'#TIME {last_written_time}\n')
                        elif raw_line.strip() == '#TIME 0':
                            f.write('#TIME 0\n')
                            current_time = 0
                        elif raw_line.strip().upper().startswith('#TIME'):
                            continue
                        elif '->' in raw_line and scene.has_fade_out and not in_choice and not printed_fade_out:
                            buffer.seek(0)
                            f.write(buffer.read())
                            f.write(f'#TIME {last_written_time + 2}\n')
                            f.write(raw_line.strip() + '\n')
                            buffer.seek(0)
                            buffer.truncate(0)
                            printed_fade_out = True
                        else:
                            buffer.write(raw_line.strip() + '\n')
                    if in_choice:
                        f.write('#TIME')
                        try:
                            while choices > 0:
                                f.write(f' {round(scene.lines[-choices].start_time, 2)}')
                                choices -= 1
                        except:
                            print(f'error in scene {scene.name} choice {scene.lines[-choices].text}')
                        f.write('\n')
                    buffer.seek(0)
                    f.write(buffer.read())
                except Exception as e:
                    print(raw_line)
                    raise e

    def load_audio_timestamps(self, use_audio=True):
        for scene in self.scenes:
            if scene.lines:
                if use_audio:
                    result = scene.get_timestamps_from_audio()
                    if not result:
                        print(f"Scene {scene.name} audio lines doesnt match scene line count")
                        scene.get_timestamps_from_csv()
                else:
                    scene.get_timestamps_from_csv()

    def generate_audio(self):
        pool = ThreadPool(6)
        pool.map(run_generate_audio, self.scenes)
        pool.close()
        pool.join()

def run_generate_audio(scene):
    if scene.rerun_audio:
        print(f'rerunning {scene.name}')
        scene.generate_audio()

class Scene:
    def __init__(self, name, lines, has_choice=False):
        self.name = name
        self.lines = lines
        self.raw_lines = []
        self.has_fade_in = False
        self.has_fade_out = False
        self.has_choice = has_choice
        self.has_choice_bug = False
        self.rerun_audio = False

    def generate_audio(self):
        audio = None
        silence = pydub.AudioSegment.silent(duration=250, frame_rate=22050)
        line_no = 0
        buffer = io.StringIO()
        buffer.write('scene_name,speaker,start_time,end_time,text\n')
        if self.has_fade_in:
            audio = pydub.AudioSegment.silent(duration=1750, frame_rate=22050)
        while line_no < len(self.lines):
            post_data = {
                'voice_settings': get_voice_settings(self.lines[line_no].person.replace(' (inner)', '')),
                'text': self.lines[line_no].text.replace('OTZ', 'OT Zed')
            }
            voice_id = get_voice_id(self.lines[line_no].person.replace(' (inner)', ''))
            response = SESSION.post(f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_22050_32', json=post_data, headers={'xi-api-key': TOKEN})
            response.raise_for_status()
            response_json = response.json()
            start_time = None
            end_time = None
            audio_bytes = io.BytesIO(base64.b64decode(response_json['audio_base64']))
            if not audio:
                audio = pydub.AudioSegment.from_file_using_temporary_files(file=audio_bytes, format='mp3')
                start_time = 0
                end_time = len(audio)
            else:
                audio = audio + silence
                start_time = len(audio) 
                audio = audio + pydub.AudioSegment.from_file_using_temporary_files(file=audio_bytes, format='mp3')
                end_time = len(audio) 
            buffer.write(f'{self.name},{self.lines[line_no].person},{start_time},{end_time},{self.lines[line_no].text.replace(",", "")}\n')
            self.lines[line_no].start_time = start_time
            self.lines[line_no].end_time = end_time
            line_no += 1
        audio = pydub.effects.compress_dynamic_range(audio)
        audio.export(f'{AUDIO_DIR}/original/{self.name}.mp3', format='mp3', tags={'track': '1', 'title':self.name})
        audio = audio.set_frame_rate(11025)
        audio.export(f'{AUDIO_DIR}/lowered_bit_rate/{self.name}.mp3', format='mp3', bitrate='16k', tags={'track': '1', 'title':self.name})
        with open(f'{TIMESTAMP_DIR}/{self.name}.csv', 'w') as f:
            buffer.seek(0)
            f.write(buffer.read())

    def get_timestamps_from_csv(self):
        if not self.lines:
            return
        with open(f'{TIMESTAMP_DIR}/{self.name}.csv', 'r') as f:
            timestamps = f.read().split('\n')[1:]
        timestamps = [timestamp for timestamp in timestamps if timestamp]
        if len(timestamps) != len(self.lines):
            print(f'{self.name} line count does not match timestamp line count')
            return 
        for line_index in range(len(self.lines)):
            self.lines[line_index].start_time = float(timestamps[line_index].split(',')[2])
            self.lines[line_index].end_time = float(timestamps[line_index].split(',')[3])
            if self.lines[line_index].text.replace(',', '').strip() != timestamps[line_index].split(',')[4]:
                print(f'{self.name} line {self.lines[line_index].text.replace(",", "").strip()} does not match {timestamps[line_index].split(",")[4]}')
            if self.lines[line_index].person != timestamps[line_index].split(',')[1].lower():
                print(f'{self.name} line {self.lines[line_index].text} speaker {self.lines[line_index].person} does not match {self.lines[line_index].person}')

    def get_timestamps_from_audio(self):
        audio = pydub.AudioSegment.from_mp3(f'{AUDIO_DIR}/original/{self.name}.mp3')
        audio = audio.set_frame_rate(11025)
        audio = pydub.effects.compress_dynamic_range(audio)
        audio = pydub.effects.normalize(audio)
        silence = pydub.AudioSegment.silent(duration=250, frame_rate=22050)
        split_audio = pydub.effects.split_on_silence(audio, silence_thresh=-1000, min_silence_len=250)
        rebuilt_audio = None
        if self.has_fade_in:
            rebuilt_audio = pydub.AudioSegment.silent(duration=1750, frame_rate=11025) 
        if len(split_audio) != len(self.lines):
            return False
        for line_index in range(len(self.lines)):
            start_time = None
            end_time = None
            if not rebuilt_audio:
                rebuilt_audio = split_audio[line_index]
                start_time = 0
                end_time = len(rebuilt_audio)
            else:
                rebuilt_audio = rebuilt_audio + silence
                start_time = len(rebuilt_audio)
                rebuilt_audio = rebuilt_audio + split_audio[line_index]
                end_time = len(rebuilt_audio)
            self.lines[line_index].start_time = start_time
            self.lines[line_index].end_time = end_time
        rebuilt_audio.export(f'{AUDIO_DIR}/new_audio/{self.name}.mp3', format='mp3', bitrate='16k', tags={'track': '1', 'title':self.name})
        return True


class Line:
    def __init__(self, person, text):
        self.person = person
        self.text = text
        self.start_time = None
        self.end_time = None


def get_voice_settings(name):
    global VOICE_SETTINGS
    return VOICE_SETTINGS[name]

def get_voice_id(name):
    global VOICES
    if not VOICES:
        response = SESSION.get('https://api.elevenlabs.io/v1/voices', headers={'xi-api-key': TOKEN})
        VOICES = response.json()
    for voice in VOICES['voices']:
        if voice['name'].lower() == name and voice['category'].lower() == 'cloned':
            return voice['voice_id']

def is_dialogue(raw_line, scene_name):
    result = False
    if len(raw_line.strip().split(':')) >= 2 and raw_line.strip()[0].isalpha():
        result = True
    elif raw_line.strip().startswith('+ [') or raw_line.strip().startswith('+['):
        result = True
    elif raw_line.strip() and raw_line.strip()[0].isalpha():
        print(f'Possible dialogue typo: {scene_name},{raw_line}')
    return result

def parse_dialogue_line(raw_line, current_speaker):
    speaker = None
    dialogue = None
    if len(raw_line.strip().split(':')) >= 2:
        speaker = raw_line.strip().split(':')[0].lower()
        dialogue = ':'.join(raw_line.strip().split(':')[1:]).strip()
    elif raw_line.strip().startswith('+ ['): 
        speaker = current_speaker
        dialogue = raw_line.strip().split('+ [')[1].split(']')[0].strip()
    elif raw_line.strip().startswith('+['):
        speaker = current_speaker
        dialogue = raw_line.strip().split('+[')[1].split(']')[0].strip()
    return Line(person=speaker, text=dialogue)
        

def parse_text_file(raw_text):
    return Act(raw_text)

def convert_audio():
    files = os.listdir(f'{AUDIO_DIR}/original/')
    for file in files:
        audio = pydub.AudioSegment.from_mp3(f'audio/original/{file}')
        audio.set_frame_rate(11025)
        audio.export(f'{AUDIO_DIR}/lowered_bit_rate/{file}', bitrate='16k', tags={'track': '1', 'title': file.split('.mp3')[0]})

def rerun_debby_scenes():
    with open('./resources/debby-rerun-scene-names.txt') as f:
        scenes_to_rerun = set([scene.replace('==', '').strip() for scene in f.read().split('\n') if scene])
        with open(f'{FILE_NAME}', mode='r') as f:
            act = parse_text_file(f.read())
            i = 0
            while i < len(act.scenes):
                if act.scenes[i].name in scenes_to_rerun: 
                    scenes_to_rerun.remove(act.scenes[i].name)
                    if not os.path.exists(f'{AUDIO_DIR}/original/{act.scenes[i].name}.mp3'):
                        rint(f'generating audio for {act.scenes[i].name}')
                        act.scenes[i].generate_audio_file()
                    else:
                        act.scenes[i].load_audio_timestamps()
                    i += 1
                elif act.scenes[i].has_choice_bug:
                    if not os.path.exists(f'{AUDIO_DIR}/original/{act.scenes[i].name}.mp3'):
                        print(f'generating audio for {act.scenes[i].name}')
                        act.scenes[i].generate_audio_file()
                    else:
                        act.scenes[i].load_audio_timestamps()
                    i += 1
                else:
                    act.scenes.pop(i)
            print(f'Remaining scenes to rerun: {scenes_to_rerun}')
            act.pre_scene_lines = []
            act.generate_ink_file()

def main():
    #convert_audio()
    with open(FILE_NAME, mode='r') as f:
        act = parse_text_file(f.read())
    act.generate_audio()
    act.load_audio_timestamps()
    act.generate_ink_file()
    #rerun_debby_scenes()



if __name__ == '__main__':
    main()
