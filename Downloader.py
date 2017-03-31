import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from selenium.webdriver.chrome.options import Options

MP3_CONVERTER = "http://www.youtube-mp3.org/"
CONVERTER2MP3 = "http://convert2mp3.net/en/index.php"
CHROME_DRIVER_PATH = ""

raw_first_line = "document.getElementById('youtube-url').value=\""
second_line = "document.getElementById(\"submit\").click();"
third_line = """for(child in document.getElementById("dl_link").childNodes)if (document.getElementById("dl_link").childNodes.hasOwnProperty(child))if(document.getElementById("dl_link").childNodes[child].style.display==""){document.getElementById("dl_link").childNodes[child].click();break;}"""

n1 = """document.getElementById(\"urlinput\").value=\""""
n2 = """document.getElementsByTagName(\"button\")[1].click();"""
n3 = """document.getElementsByTagName(\"a\")[12].click();"""
n4 = """document.getElementsByTagName(\"a\")[9].click();"""
n5 = """document.getElementsByTagName(\"span\")[0].click();"""
n6 = """document.getElementsByTagName(\"a\")[9].click();"""


def mode2(driver, song,fails):
    first_line = raw_first_line + song.strip('\n') + "\";"
    driver.execute_script(first_line)
    driver.execute_script(second_line)
    time.sleep(4)

    if not driver.find_element_by_id("error_text").is_displayed():
        driver.execute_script(third_line)
    else:
        print(song, end="")
        fails.write(song)


def mode1(driver, song, fails):
    first_line = n1 + song.strip('\n') + "\";"
    driver.execute_script(first_line)
    driver.execute_script(n2)
    time.sleep(7)
    try:
        driver.find_element_by_id("errormsg")
        print(song, end="")
        fails.write(song)
    except NoSuchElementException:
        driver.execute_script(n3)
        time.sleep(1)
        driver.execute_script(n4)
        if i == 2:
            time.sleep(5)
        driver.execute_script(n5)


SITE = {1: CONVERTER2MP3, 2: MP3_CONVERTER}
DOWNLOAD = {1: mode1, 2: mode2}


def downloader(driver,mode, list_of_songs, stop=""):
    with open(list_of_songs, "r", encoding="Utf-8-sig") as songs, open("fails.txt", "a", encoding="Utf-8-sig") as fails:
        for song in songs:
            if song.strip('\n') == stop:
                break
            DOWNLOAD[mode](driver, song, fails)
            



def main():
    if len(sys.argv) != 4:
        sys.exit(1)
    mode = sys.argv[1]
    songs_list = sys.argv[2]
    download_directory = sys.argv[3]
    options = Options()
    options.add_experimental_option('prefs', {'download.default_directory': download_directory})
    options.add_argument("--disable-infobars")
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, chrome_options=options)
    driver.get(SITE[mode])
    try:
        downloader(driver,mode, songs_list)
    except NoSuchWindowException:
        pass
    finally:
        time.sleep(50)
        driver.close()
        exit()


if __name__ == '__main__':
    main()
