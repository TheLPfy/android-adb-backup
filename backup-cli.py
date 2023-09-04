import os
from ppadb.client import Client as AdbClient
import sys
from yaspin import yaspin
from datetime import datetime

def read_adb_file_lines(file, adb):
    dest = os.path.join(os.getcwd(), os.path.basename(file))
    adb.pull(file, dest)
    with open(dest) as file:
        lines = [line.rstrip() for line in file]
    if check_file_exists(dest):
        os.remove(dest)
    return lines



def get_files(adb):
    with yaspin(text="Loading...", color="yellow", timer=True) as spinner:
        spinner.text = "Retrieving files..."
        # find should be available on all phones
        # /sdcard is the internal storage
        # type f includes only files
        # \( \) is used to define multiple arguments and -name searches for spefic file endings (NOT REGEX!) and -o means OR
        # 2>&1 redirects the error and the these lines with "Permission denied are filtered out"
        adb.shell('rm -f /sdcard/backup_images.out')
        adb.shell('find /sdcard/ -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.mp4" -o -name "*.m4a" \) -not -path "/sdcard/Android/*" 2>&1 | grep -v "Permission denied" > /sdcard/backup_images.out')
        # All images are seperated by a \n
        images = read_adb_file_lines("/sdcard/backup_images.out", adb)
        spinner.write("> " + str(len(images)) + " files retrieved")
        spinner.text = "Getting modification date..."
        adb.shell('rm -f /sdcard/backup_unix.out')
        adb.shell('tr "\n" "\0" < /sdcard/backup_images.out | xargs -0 stat -c %Y > /sdcard/backup_unix.out')
        mod_unix = read_adb_file_lines("/sdcard/backup_unix.out", adb)
        spinner.write("> " + str(len(mod_unix)) + " stats gathered")
        if len(images) != len(mod_unix):
            sys.exit("files and stats do not match!")
        spinner.text = "Getting files"
        spinner.ok("✔")
    return dict(zip(images, mod_unix))


def check_file_exists(path):
    if not os.path.isfile(path):
        return False
    # Check if file has data
    return os.path.getsize(path) != 0


def download_files(path, images, adb):
    with yaspin(text="Pulling files...", color="yellow", timer=True) as spinner:
        for image, unix in images.items():
            folder = datetime.utcfromtimestamp(int(unix)).strftime('%Y/%m')
            image_name = os.path.basename(image)
            dest = os.path.join(path, folder, image_name)
            if check_file_exists(dest):
                spinner.write("> Skipping file " + str(image) + " already in " + dest)
                continue
            spinner.write("> Pulling file " + str(image) + " to " + dest)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            adb.pull(image, dest)
        spinner.ok("✔")


def adb_connect():
    os.system("adb devices")

    client = AdbClient(host="127.0.0.1", port=5037)

    devices = client.devices()

    try:
        device = devices[0]
        return device
    except:
        print(f"Device not found.\n{devices}")
        return None


def main():
    adb = adb_connect()

    if adb is None:
        sys.exit("ADB failure")

    images_unix_dict = get_files(adb=adb)

    download_files(path=os.getcwd(), images=images_unix_dict, adb=adb)


if __name__ == '__main__':
    main()
