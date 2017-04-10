import sys
from tkinter.filedialog import askdirectory, askopenfilename

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, WebDriverException

from downloader import downloader
from downloader import logger


FIREFOX_DRIVER_PATH = "C:\\Users\\QAZ\\Videos\\geckodriver.exe"
CONVERTER2MP3 = "http://convert2mp3.net/en/index.php"
MP3_CONVERTER = "http://www.youtube-mp3.org/"
WEBSITE = {"1": CONVERTER2MP3, "2": MP3_CONVERTER}


def get_firefox_profile(download_directory):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("dom.popup_maximum", 0)
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", download_directory)
    profile.set_preference("browser.download.panel.shown", False)
    profile.set_preference("privacy.popups.showBrowserMessage", False)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ".mp3 audio/mpeg")
    return profile


def get_user_choice():
    input("press enter when ready to choose the list of songs")
    songs_list = askopenfilename(initialdir='.')
    if not songs_list:
        raise ValueError("You did not choose the songs list file.")
    if not songs_list.endswith("txt"):
        raise ValueError("A text file must be chosen.")

    input("press enter when ready to choose the download directory")
    download_directory = askdirectory(initialdir='.')
    if not download_directory:
        raise ValueError("You did not choose the download directory.")
    return songs_list, download_directory


def main():
    if len(sys.argv) != 2:
        print("Incorrect number of arguments")
        print("""You need to choose one of the following modes:\n1 - Downloading the songs from converter2mp3.\n2 - 
            Downloading the songs from mp3 converter.""")
        sys.exit(1)
    mode = sys.argv[1]
    try:
        songs_list, download_directory = get_user_choice()
    except ValueError as e:
        print(e)
        logger.exception(e)
        sys.exit(1)
    print("Starting to download songs...")
    try:
        profile = get_firefox_profile(download_directory)
        driver = webdriver.Firefox(firefox_profile=profile, executable_path=FIREFOX_DRIVER_PATH)
        driver.get(WEBSITE[mode])
        downloader(driver, mode, songs_list)
    except (WebDriverException, NoSuchWindowException) as e:
        logger.exception(e)
        sys.exit(1)
    else:
        driver.close()
        sys.exit(0)


if __name__ == '__main__':
    main()
