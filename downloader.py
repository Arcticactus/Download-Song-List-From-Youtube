import time
import logging
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LOGGER.setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
logging.basicConfig(filename="failed_songs.log", level=logging.DEBUG)

ENTER_SONG_NAME = """document.getElementById("youtube-url").value="{}";"""
SUBMIT_SONG = """document.getElementById("submit").click();"""
PRESS_DOWNLOAD = """for(child in document.getElementById("dl_link").childNodes)if (document.getElementById("dl_link").childNodes.hasOwnProperty(child))if(document.getElementById("dl_link").childNodes[child].style.display==""){document.getElementById("dl_link").childNodes[child].click();break;}"""

INSERT_SONG_NAME = """document.getElementById("urlinput").value="{}";"""
CONVERT_SONG = """document.getElementsByTagName("button")[1].click();"""
SKIP_TAGS = """document.getElementsByTagName("a")[12].click();"""
DOWNLOAD_SONG = """document.getElementsByTagName("a")[9].click();"""
CONVERT_NEXT = """document.getElementsByTagName("span")[0].click();"""
n6 = """document.getElementsByTagName("a")[9].click();"""


def download_mp3_converter(driver, song):
    driver.execute_script(ENTER_SONG_NAME.format(song))
    driver.execute_script(SUBMIT_SONG)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "dl_link")))
    driver.execute_script(PRESS_DOWNLOAD)


def download_converter2mp3(driver, song):
    def execute(web_driver, command):
        web_driver.execute_script(command)
        time.sleep(3)

    driver.execute_script(INSERT_SONG_NAME.format(song))
    driver.execute_script(CONVERT_SONG)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "advancedtags_btn")))
    execute(driver, SKIP_TAGS)
    execute(driver, DOWNLOAD_SONG)
    execute(driver, CONVERT_NEXT)


DOWNLOAD_FUNCTIONS = {"1": download_converter2mp3, "2": download_mp3_converter}


def downloader(driver, mode, songs_list):
    download_song = DOWNLOAD_FUNCTIONS[mode]
    with open(songs_list, "r", encoding="utf-8-sig") as songs:
        for song in songs:
            try:
                download_song(driver, song.strip("\n"))
            except (TimeoutException, NoSuchElementException):
                logger.warning(" Failed to download: " + song.strip("\n"))
