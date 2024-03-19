import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import requests
import re
import urllib3
from dotenv import load_dotenv

load_dotenv()

# ignore ssl verify errors, cause they are annoying AF
urllib3.disable_warnings()


def upload(file):
    auth = (os.getenv('MEDIACMS_USER'), os.getenv('MEDIACMS_PASSWORD'))
    print('auth ', auth)
    print('file: ', file)
    x = re.findall("[^\.\/]+(?=\.)", file)
    title = x[0]
    description = ''
    media_file = file
    print('Uploading ', media_file)
    try:
        resp = requests.post(
            url=os.getenv('MEDIACMS_URL'),
            files={'media_file': open(media_file,'rb')},
            data={'title': title, 'description': description},
            auth=auth,
            verify=False)
        
        if resp.ok:
            try:
                print('deleting file...')
                os.remove(media_file)
            except OSError:
                pass

    except requests.exceptions.HTTPError as err:
        print(err)

class Watcher:
    # DIRECTORY_TO_WATCH = "../nginx-rtmp/videos"
    DIRECTORY_TO_WATCH = os.getenv('WATCH_FOLDER')

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_closed(event):
        file_size = -1
        while file_size != os.path.getsize(event.src_path):
            file_size = os.path.getsize(event.src_path)
            print("file size: ", file_size)
            time.sleep(1)

        if event:
            print("file created:{}".format(event.src_path))
            print("Finished event - %s." % event.src_path)
            print("uploading to mediacms - %s." % event.src_path)
            upload(event.src_path)


if __name__ == '__main__':
    w = Watcher()
    print('Watcher watching...')
    w.run()
