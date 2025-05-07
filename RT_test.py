from RealtimeSTT import AudioToTextRecorder
from colorama import Fore, Style
import colorama
import os

if __name__ == '__main__':

    print("Initializing RealtimeSTT test...")

    colorama.init()

    full_sentences = []
    displayed_text = ""

    def clear_console():
        os.system('clear' if os.name == 'posix' else 'cls')

    def text_detected(text):
        try:

            global displayed_text
            sentences_with_style = [
                f"{Fore.YELLOW + sentence + Style.RESET_ALL if i % 2 == 0 else Fore.CYAN + sentence + Style.RESET_ALL} "
                for i, sentence in enumerate(full_sentences)
            ]
            new_text = "".join(sentences_with_style).strip() + " " + text if len(sentences_with_style) > 0 else text

            if new_text != displayed_text:
                displayed_text = new_text
                clear_console()
                print(displayed_text, end="", flush=True)
                
        except Exception as e:
            print(e)

    last_text = ""

    def process_text(text):
        global last_text
        if text.strip() == last_text.strip():
            return
        last_text = text.strip()

        # 콘솔 클리어하고 마지막 문장만 출력
        clear_console()
        print(Fore.GREEN + text.strip() + Style.RESET_ALL, end="", flush=True)


    recorder_config = {
    'spinner': False,
    'model': 'turbo',
    'language': 'ko',
    'silero_sensitivity': 0.7,
    'webrtc_sensitivity': 1,
    'post_speech_silence_duration': 0.8,  # 조금 더 기다림
    'min_length_of_recording': 0,
    'min_gap_between_recordings': 0,  # 바로 다시 시작하지 않게

    'enable_realtime_transcription': True,
    'realtime_processing_pause': 0.3,
    # 'realtime_model_type': 'base',
    'on_realtime_transcription_update': None, #text_detected
    'on_realtime_transcription_stabilized': process_text,
}




    recorder = AudioToTextRecorder(**recorder_config)

    clear_console()
    print("Say something...", end="", flush=True)

    while True:
        text = recorder.text(process_text)
        text_detected(text)