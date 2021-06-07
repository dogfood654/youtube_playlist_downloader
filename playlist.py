# MUSIC DOWNLOADER FROM YOUTUBE

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=25,
        # Change this to change to different playlist
        playlistId="PL9qRRUpuq7Gmr1hDXDseDEgAQbsns0aeF"
    )
    response = request.execute()

    playlist_list = []
    for item in response["items"]:
        contentDetails = item["contentDetails"]
        playlist_list.append(contentDetails["videoId"])
    print(playlist_list)
    converter(playlist_list)

def converter(playlist_list):

    url_songs = playlist_list

    driver = webdriver.Chrome(executable_path="D:\\chromedriver_win32\\chromedriver.exe")
    driver.get("https://yt1s.com/youtube-to-mp3/en2")

    for song in url_songs:

        time.sleep(1)
        searchbox = driver.find_element_by_xpath("//*[@id='s_input']")
        searchbox.send_keys("https://www.youtube.com/watch?v=" + song)

        searchbutton = driver.find_element_by_xpath("//*[@id='search-form']/button")
        searchbutton.click()

        wait = WebDriverWait(driver, 30)
        element = wait.until(EC.element_to_be_clickable((By.ID, "asuccess")))
        downloadbutton = driver.find_element_by_id("asuccess")
        downloadbutton.click()

        driver.get("https://yt1s.com/youtube-to-mp3/en2")
        # time.sleep(1)
        # homebutton = driver.find_element_by_xpath("//*[@id='navbar']/ul/li[2]/a")
        # homebutton.click()

        print(song)
    
    time.sleep(60*60)

if __name__ == "__main__":
    main()