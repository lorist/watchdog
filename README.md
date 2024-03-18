# video watchdog

A simple Python app that watches a folder for new files, uploads them to MediaCMS then deletes the local copy.

## Installation

1. Clone this repo
2. Create a file in the watchdog folder called `.env`
    In this file, add environment variables that the docker container will use to upload files to MediaCMS.
    Example:
        ```
        MEDIACMS_USER='admin'
        MEDIACMS_PASSWORD='password'
        MEDIACMS_URL='https://mediacms.example.com/api/v1/media'
        WATCH_FOLDER='../nginx-rtmp/videos'
        ```
3. Build and run the container: 
        ```
        docker compose build
        docker compose up -d
        ```
