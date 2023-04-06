import openai
import traceback
import argparse
import os, sys

from dotenv import load_dotenv
from pydub import AudioSegment
from typing import List, Any

load_dotenv()

# openai.api_key = os.environ['OPENAI_API_KEY']
if not os.getenv('OPENAI_API_KEY'):
    print('Missing OPENAI_API_KEY')
    sys.exit(1)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

                                
OUTPUT_PATH = 'output_split_sound/'
TIME_MINUTE = 60 * 1000
TEN_MINUTES = 10 * TIME_MINUTE

def open_media(path: str):
    try:
        print('Carregando ao arquivo de mídia...')
        audio_file_import = AudioSegment.from_mp3(path)
        return audio_file_import
    except Exception:
        print('Erro ao carregar o arquivo de mídia')
        traceback.print_exc()
    finally: print('Mídia carregada com sucesso!')

def create_folder(out_directory: str) -> str:
    if not os.path.exists(out_directory):
        os.makedirs(out_directory)
        return out_directory
    else:
        num_label_dir = 1

        while True: # enquanto o nome existir, continue

            out_directory_numbered = out_directory + '-' + str(num_label_dir)

            if not os.path.exists(out_directory_numbered):
                os.makedirs(str(out_directory + '-' + str(num_label_dir)))
                return out_directory_numbered
            else:
                num_label_dir = num_label_dir + 1


def split_media(media: Any, label: str, out_dir: str) -> str and List[str]:

     
    try:
        print('Iniciando o fatiamento da mídia...')
        path_tracks: List[str] = []

        duration_ms_media: int = len(media) # Duração da mídia em ms
        duration_min_media: float  = duration_ms_media / TIME_MINUTE # Duração mídia em min 
        number_intervals: float = duration_min_media / 10 # Numero de intervalos | fatias
        number_intervals_normalized: int = int(round(number_intervals, 2))+1 # intervalo + 1

        out_directory = out_dir + '-' + label
        current_out_directory = create_folder(out_directory)

        for i in range(number_intervals_normalized):
            print('Corte',  i + 1, ' de ', number_intervals_normalized)

            start_time = TEN_MINUTES * i
            end_time = TEN_MINUTES * (i + 1)

            slice_track = media[start_time:end_time]
            
            path_tack = str(current_out_directory + '/' + label + '-' + str(i) + '.mp3')

            slice_track.export(path_tack, format="mp3")
            path_tracks.append(path_tack)
        
        return current_out_directory, path_tracks # Retorna a o dir de saida e o local das mídias fatiados

    except Exception:
        print('Erro ao fatiar a mídia')
        traceback.print_exc()

    finally:
        print('Fatiamento finalizado!')

def write_file(path: str, text_file: str):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(text_file)
    except Exception:
        print('Erro ao salvar o arquivo: ', path)
        traceback.print_exc()

def create_text(out_directory: str, path_tracks: List[str], label: str) -> None:
    print('Iniciando a transcrição da mídia...')

    for index, path in enumerate(path_tracks):
        try:
            print('Transcrição do corte ',  index+1, ' de ', len(path_tracks))
            audio_file= open(path, "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file, response_format="text")
            print('Transcrição concluida!')
            path_text_out = str(out_directory + '/' + label + '-' + str(index) + '-text-out.txt')
            print('Salvando a transcrição!')

            write_file(path_text_out, transcript)

        except FileNotFoundError:
            print('Arquivo de mídia não foi encontrado!')
            traceback.print_exc()


def main(args):

    file = args.file
    label = args.label
    out_dir = args.out_dir


    audio = open_media(file)
    current_out_directory, path_tracks = split_media(audio, label, out_dir)

    create_text(current_out_directory, path_tracks, label)
    print("Finalizado!")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Use OpenAI Whisper para extrar texto de áudio e video')
    parser.add_argument('--file', type=str, required=True, help="O áudio ou video que vai ser extraido o texto")
    parser.add_argument('--label', type=str, required=True, help="Label identificar a resposta gerada")
    parser.add_argument('--out-dir', type=str, required=False, help="Diretório onde vai salvar o arquivo de saída", default="output")
   
    args = parser.parse_args()

    main(args)

