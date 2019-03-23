# YouTube Mass Downloader:
Downloads a list of YouTube songs (by URL) to a chosen directory (downloads audio only as mp3)

# Usage:
1. Create a `txt` file which contains the URL's you wish to download.
2. Run the code.
3. Choose 1 to download from converter2mp3 and 2 to download from mp3 converter.
4. Select the `txt` file from step 1 using the Windows explorer.
5. Select the directory to which the files will be downloaded using the Windows explorer.
6. Wait while the files are being downloaded, make sure to be connected to the internet at all times.
7. Upon completion, review `failed_songs.log to` for the list of songs that failed to download (usually because the URL is no longer valid).

# Notes:
The code uses selenium and Firefox gecko drive, due to recent changes in Firefox the code can no longer works.
