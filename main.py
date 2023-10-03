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
USERNAME = ''
PASSWORD = ''

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


def login(username, password):
    # Do a session.get here so that we get a csrf_cookie_name cookie
    SESSION.get("https://aivoov.com/signin")
    headers = {`
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            'Accept-Encoding': 'gzip, deflate, br',
            "Cache-Control": 'max-age=0',
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "aivoov.com",
            "Origin": "https://aivoov.com",
            "Referer": "https://aivoov.com/signin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    login_data = {"username": username, "password": password, "base_url": "https://aivoov.com", "csrf_test_name": [SESSION.cookies['csrf_cookie_name'], SESSION.cookies['csrf_cookie_name']]}
    response = SESSION.post('https://aivoov.com/authentication/signin_do/', headers=headers, data=login_data)
    if response.status_code >= 400:
        raise Exception(response.text)


def create_audio_file(scene):
    print(f"uploading scene {scene.name}")

    post_data = {
        'csrf_test_name': SESSION.cookies['csrf_cookie_name'],
        'transcribe_text_title': scene.name,
        'projects': PROJECT_ID,
        'transcribe_auto_save_id': '', 
        'transcribe_text_used_value': '', 
        'check_slug': '', 
        'transcribe_type': 'text',
        'auto_save': 1,
        'synthesize_type': 'save',
        'transcribe_text_input_position': '',
        'project_hash_key': '',
        'editor_v': 2,
        'language_init': [],
        'default_language_id[]': [],
        'default_scheme': [],
        'transcribe_filter_voice[]': [],
        'transcribe_ssml_style[]': [],
        'transcribe_ssml_volume[]': [],
        'transcribe_ssml_spk_rate[]': [],
        'transcribe_ssml_pitch_rate[]': [],
        'transcribe_text[]': []
    }
    for line in scene.lines:
        post_data['language_init'].append('')
        post_data['default_language_id[]'].append(PEOPLE_TO_VOICE_MAP[line.person])
        post_data['default_scheme'].append('')
        post_data['transcribe_filter_voice[]'].append('neural')
        post_data['transcribe_ssml_style[]'].append('')
        post_data['transcribe_ssml_spk_rate[]'].append('default')
        post_data['transcribe_ssml_pitch_rate[]'].append('default')
        post_data['transcribe_text[]'].append(f'<p>{line.text}</p>')
    
    response = SESSION.post('https://aivoov.com/transcribe/get_transcribe_beta/', data=post_data)


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
    login(USERNAME, PASSWORD)
    for scene in act.scenes:
        create_audio_file(scene)


if __name__ == '__main__':
    main()
