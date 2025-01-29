import base64
import os
import subprocess
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tqdm import tqdm

from base import BasePage
from waiting_module.waiter import wait_for_visible

email = ""
password = ""
main_url = ""
# lesson_names = list(range(41, 64))


class BPLocators:
    EMAIL_INPUT = By.XPATH, "//input[@name='login']"
    PASSWORD_INPUT = By.XPATH, "//input[@name='password']"
    LOGIN_BUTTON = By.XPATH, "//button[@class='main-button']"
    PLAY_BUTTON = By.XPATH, "//button[@class='plyr__control plyr__control--overlaid']"


def download(what, to, base):
    print('saving', what['mime_type'], 'to', to)
    with open(to, 'wb') as file:
        init_segment = base64.b64decode(what['init_segment'])
        file.write(init_segment)

        for segment in tqdm(what['segments']):
            segment_url = base + segment['url']
            resp = requests.get(segment_url, stream=True)
            if resp.status_code != 200:
                print('not 200!')
                print(segment_url)
                break
            for chunk in resp:
                file.write(chunk)
    print('done')


def fetch_json():
    time.sleep(3)
    subprocess.Popen([r".venv\Scripts\python.exe", r".venv\Scripts\mitmdump.exe", "-s", "fetch_json.py"],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)


def kill_processes_using_port(port):
    # Run netstat command to find processes using the given port
    netstat_command = f'netstat -ano | findstr :{port}'

    try:
        # Execute the netstat command and capture the output
        result = subprocess.check_output(netstat_command, shell=True, text=True)

        if not result.strip():  # Check if result is empty (no processes found)
            print(f"No processes found using port {port}.")
            return

        # Process each line in the output
        for line in result.splitlines():
            # Split the line by spaces to get the PID (which is the 5th token)
            tokens = line.split()
            if len(tokens) > 4:
                pid = tokens[4]

                # Kill the process using the PID
                kill_command = f'taskkill /PID {pid} /F'
                print(f"Running: {kill_command}")  # Debugging output
                subprocess.run(kill_command, shell=True)
                print(f"Killed process with PID: {pid}")

    except subprocess.CalledProcessError as e:
        print(f"Error executing netstat command: {e}")
        print(f"Command output: {e.output}")
    except Exception as e:
        print(f"An error occurred: {e}")


def download_and_combine_video_audio(lesson_name):
    video_file = 'video.mp4'
    audio_file = 'audio.mp4'
    json_file = 'json_link.log'

    options = Options()
    options.add_argument("--proxy-server=http://localhost:8080")
    options.add_argument("--mute-audio")
    options.add_argument("--headless")  # Run in headless mode
    # options.add_argument("--window-size=1920,1080")  # (Optional) Set window size
    driver = webdriver.Chrome(service=Service(), options=options)

    session = BasePage(driver)
    session.open(main_url.format(lesson_name))

    wait_for_visible(driver, BPLocators.EMAIL_INPUT, timeout=60)
    session.set_text(BPLocators.EMAIL_INPUT, email)
    session.set_text(BPLocators.PASSWORD_INPUT, password)
    session.click(BPLocators.LOGIN_BUTTON)
    wait_for_visible(driver, BPLocators.PLAY_BUTTON, timeout=60)
    session.click(BPLocators.PLAY_BUTTON)

    # Wait for some time to let the media load
    time.sleep(15)

    driver.quit()

    with open(json_file, "r") as f:
        url = f.readline().strip()
        print(url)

    base_url = url[:url.rfind('/', 0, -26) + 1]
    content = requests.get(url).json()

    vid_heights = [(i, d['height']) for (i, d) in enumerate(content['video'])]
    vid_idx, _ = max(vid_heights, key=lambda _h: _h[1])

    audio_quality = [(i, d['bitrate']) for (i, d) in enumerate(content['audio'])]
    audio_idx, _ = max(audio_quality, key=lambda _h: _h[1])

    video = content['video'][vid_idx]
    audio = content['audio'][audio_idx]
    base_url = base_url + content['base_url']

    download(video, video_file, base_url + video['base_url'])
    download(audio, audio_file, base_url + audio['base_url'])

    ffmpeg_path = r"ffmpeg\bin\ffmpeg.exe"
    subprocess.run([
        ffmpeg_path, "-i", video_file, "-i", audio_file,
        "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", f"{lesson_name}.mp4"
    ], check=True)

    os.remove(video_file)
    os.remove(audio_file)
    os.remove(json_file)


# Loop through multiple lessons
for lesson_name in lesson_names:
    kill_processes_using_port(8080)
    fetch_json()  # Restart the proxy before each lesson
    download_and_combine_video_audio(lesson_name)