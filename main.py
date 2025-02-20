import base64
import os
import pydub
import requests

FILE_NAME = '/home/nick/code/aivoov/simon_2.txt'
MALE_VOICE = 'd7c2b60e-185b-4447-902f-2283c4afa876' 
FEMALE_VOICE = 'f2bc131c-436b-4581-97d0-28fb9e6e35e2'
PEOPLE_TO_VOICE_MAP = {
          'mercy (inner)': FEMALE_VOICE, 
          'mercy': FEMALE_VOICE, 
          'faith': FEMALE_VOICE, 
          'vivian': FEMALE_VOICE, 
          'sally': FEMALE_VOICE,
          'adhiambo': FEMALE_VOICE,
          'dr. atieno': FEMALE_VOICE,
          'simon’s mum':FEMALE_VOICE,
          'mercy father': MALE_VOICE,
          'father': MALE_VOICE,
          'john': MALE_VOICE,
          'george': MALE_VOICE,
          'peter': MALE_VOICE,
          'james': MALE_VOICE,
          'erick': MALE_VOICE,
          'otis': MALE_VOICE,
          'simon': MALE_VOICE,
          'simon (inner)': MALE_VOICE
        }
PROJECT_ID = '3efd4607-c137-4920-93f4-0bec86dfeabb'
#Mercy act 1 8451fe01-9d06-4b96-aca2-22e6778ad90d
#Mercy act 2 a12dbe3b-a24c-422d-a7ef-298fa56a92cb
#Simon act 2 3efd4607-c137-4920-93f4-0bec86dfeabb
TOKEN = os.environ['TOKEN']
VOICES = None
SESSION = requests.Session()
SCENE_NAMES = set()

class Act:
    def __init__(self, data):
        self.scenes = []
        current_scene = None
        current_speaker = None
        for raw_line in data.split('\n'):
            if raw_line.startswith('=='):
              if current_scene and not current_scene.lines:
                    self.scenes.remove(current_scene)
                    print(f'Removing scene {current_scene.name}')
              current_scene = Scene(name=raw_line.split('==')[1].strip(), lines=[])
              if current_scene.name in SCENE_NAMES:
                  print(f"ERROR DUPLICATE SCENE NAME {current_scene.name}")
              else:
                SCENE_NAMES.add(current_scene.name)
              if ' ' in raw_line.split('==')[1].strip():
                  print(f"Error space in scene name {current_scene.name}")
              self.scenes.append(current_scene)
            elif raw_line.strip().startswith('*['):
                current_scene.has_choice = True
                choice_text = raw_line.strip().split('*[')[1].split(']')[0].strip()
                current_scene.lines.append(Line(person=current_speaker, text=choice_text))
            elif '->' in raw_line.strip():
                pass
            elif raw_line.strip().startswith('VAR'):
                pass
            elif raw_line.strip().startswith('['):
                pass
            elif raw_line.strip().startswith('#'):
                pass
            elif raw_line.strip().startswith('{'):
                pass
            elif raw_line.strip().startswith('}'):
                pass
            elif raw_line.strip().startswith('~'):
                pass
            elif raw_line.strip().startswith('_________________________________________________________________________________'):
                pass
            elif not raw_line.strip():
                pass
            elif len(raw_line.strip().split(':')) >= 2:
                dialogue = raw_line.strip().split(':')
                person = dialogue[0].lower()
                text = dialogue[1]
                if person not in PEOPLE_TO_VOICE_MAP.keys():
                    print(f"ERROR, {person} not in text map")
                current_speaker = person
                current_scene.lines.append(Line(person=person, text=text.replace('(', '').replace(')', '')))
            else:
                print(f"Error, couldn't parse: =={current_scene.name}== line: {raw_line}")
        if current_scene and not current_scene.lines:
            self.scenes.remove(current_scene)
            print(f'Removing scene {current_scene.name}')


class Scene:
    def __init__(self, name, lines, has_choice=False):
        self.name = name
        self.lines = lines
        self.has_choice = has_choice


class Line:
    def __init__(self, person, text):
        self.person = person
        self.text = text


def create_audio_file(scene):
    audio = None
    post_data = {
        'model_id' :'eleven_multilingual_v2'
    }
    line_no = 0
    audio_length = 0.0
    silence = pydub.AudioSegment.silence(duration=250)
    while line_no < len(scene.lines):
        post_data['text'] = scene.lines[line_no].text
        if line_no != 0:
            post_data['previous_text'] = scene.lines[line_no-1].text
        if line_no != len(scene.lines) - 1:
            post_data['next_text'] = scene.lines[line_no+1].text
        voice_id = get_voice_id(scene.lines[line_no].person.remove(' (inner)'))
        response = SESSION.post(f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128', data=post_data, headers={'xi-api-key': TOKEN})
        response.raise_for_error()
    
        response_json = response.json()
        if not audio:
            audio = pydub.AudioSegment(data=bytes(base64.b64decode(response_json['audio_base64'])), frame_rate=44100)
            audio_length = response_json["alignment"]["character_end_times_seconds"][-1] 
            print(f'{scene.name},{scene.lines[line_no].person},0.00,{audio_length},{scene.lines[line_no].text.replace(",", "")}')
        else:
            audio = audio + silence + pydub.AudioSegment(data=bytes(base64.b64decode(response_json['audio_base64'])), frame_rate=44100)
            length = response_json["alignment"]["character_end_times_seconds"][-1]
            print(f'{scene.name},{scene.lines[line_no].person},{audio_length+.25},{audio_length+.25+length},{scene.lines[line_no].text.replace(",", "")}')
            audio_length = audio_length + length + .25
        line_no += 1
    with open(f'{scene.name}.mp3', 'rwb') as f:
        f.write(audio)


def get_voice_id(name):
    if not VOICES:
        response = SESSION.get('https://api.elevenlabs.io/v1/voices', data=post_data, headers={'xi-api-key': TOKEN})
        VOICES = response.json()
    for voice in VOICES['voices']:
        if voice['name'].lower() == name:
            return voice['voice_id']


def parse_text_file(raw_text):
    return Act(raw_text)


def generate_ink_file(raw_text):
    with open(FILE_NAME + '.ink', mode='w') as f:
        for raw_line in raw_text.split('\n'):
            if raw_line.startswith('=='):
                f.write(raw_line.strip() + '\n')
                if ' ' in raw_line.split('==')[1].strip():
                    print(f"Error space in scene name {current_scene.name}")
            elif raw_line.strip().startswith('*['):
                f.write(raw_line.strip() + '\n')
            elif raw_line.strip().startswith('VAR'):
                f.write(raw_line.strip() + '\n')
            elif '->' in raw_line.strip():
                f.write(raw_line.strip() + '\n')
            elif raw_line.strip().startswith('['):
                f.write(raw_line.strip() + '\n')
            elif raw_line.strip().startswith('{'):
                f.write(raw_line.strip() + '\n')
            elif raw_line.strip().startswith('}'):
                f.write(raw_line.strip() + '\n')
            elif raw_line.strip().startswith('~'):
                f.write(raw_line.strip() + '\n')
            elif raw_line.strip().startswith('_________________________________________________________________________________'):
                pass
            elif not raw_line.strip():
                f.write(raw_line.strip() + '\n')
            elif len(raw_line.strip().split(':')) >= 2:
                dialogue = raw_line.strip().split(':')
                person = dialogue[0].lower()
                text = dialogue[1].strip()
                if person not in PEOPLE_TO_VOICE_MAP.keys():
                    print(f"ERROR, {person} not in text map")
                f.write(dialogue[1] + '\n\n')
            else:
                print(f"Error, couldn't parse: line: {raw_line}")


def main():
    with open(FILE_NAME, mode='r') as f:
        act = parse_text_file(f.read())
    with open(FILE_NAME, mode='r') as f:
        generate_ink_file(f.read())
    for scene in act.scenes:
        print('scene_name,speaker,start_time,end_time,text')
        create_audio_file(scene)


if __name__ == '__main__':
    main()
