import os
import sys
import time
import logging
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


source_dir = "/home/cameron/Downloads"
dest_dir_images = "/home/cameron/Pictures"
dest_dir_scripts = "/home/cameron/Scripts"

def makeUnique(path):
    filename, extension = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = filename + " (" + str(counter) + ") " + extension
        counter += 1

def move(dest, entry, name):
    file_exists = os.path.exists(dest + "/" + name)
    if file_exists:
        unique_name = makeUnique(name)
        os.rename(entry, unique_name)
    shutil.move(entry,dest)


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                dest = source_dir
                if name.endswith('.png') or name.endswith('.jpg') or name.endswith('.jpeg'):
                    dest = dest_dir_images
                    move(dest, entry, name)
                elif name.endswith('.py') or name.endswith('.sh'):
                    dest = dest_dir_scripts
                    move(dest, entry, name)

                    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()