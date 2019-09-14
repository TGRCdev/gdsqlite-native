import boto3
import sys
import subprocess
import threading
import shutil
import zipfile
import os
from colorama import Fore, Back
from colorama import init as colorama_init
colorama_init(autoreset=True)

def wait_and_download_thread(binary_name, bucket_name, folder, logger):
    s3 = boto3.resource("s3")
    s3_obj = s3.Object(bucket_name, folder + binary_name)
    while True:
        try:
            s3_obj.wait_until_exists()
            break
        except boto3.exceptions.botocore.exceptions.WaiterError:
            pass
    logger.update(binary_name)
    s3_obj.download_file("bin/" + binary_name)
    logger.update(binary_name)

if "--help" in sys.argv or '-h' in sys.argv:
    print("Usage: python create_nightly.py [options]")
    print("Downloads the compiled binaries of the latest (or defined) commit to the nightly branch and zips them into an archive.")
    print("Valid options:")
    print("--commit, -c <hash>\n\tCreates a nightly for the given hash, assuming it is on the nightly branch.")
    print("--help, -h\n\tPrints this help message.")
    print("--upload, -u\n\tUploads the resulting zip file to S3")
    print("--fat-zip\n\tDoesn't compress the resulting zip. Used for testing")
    print("--skip-download\n\tDoes not download the binaries from S3.")
    print("--skip-zip\n\tDoes not zip up the binaries.")
    exit()

# Step 1: Get the latest commit of the nightly branch, or the commit given in command line options
commit = ""
if "--commit" in sys.argv:
    commit = sys.argv[sys.argv.index("--commit") + 1]
elif "-c" in sys.argv:
    commit = sys.argv[sys.argv.index("-c") + 1]
else:
    result = subprocess.run(['git', 'rev-parse', 'HEAD'], stdout=subprocess.PIPE)
    commit = result.stdout.decode('utf-8').replace('\n', '').replace('\r','').strip()
short = commit[:7]
print("%sNIGHTLY COMMIT HASH: %s%s (%s)" % (Fore.CYAN, Fore.LIGHTYELLOW_EX, commit, short))

# Step 2: Setup S3
s3 = boto3.resource('s3')
bucket = s3.Bucket('tgrcdev-nightlys')
bucket.wait_until_exists()

# Step 3: Find binaries
binary_list = ['gdsqlite.64.dll', 'gdsqlite.32.dll', 'libgdsqlite.64.so', 'libgdsqlite.32.so', 'libgdsqlite.64.dylib', 'libgdsqlite.armv7.so', 'libgdsqlite.arm64v8.so', 'libgdsqlite.x86.so', 'libgdsqlite.x86_64.so']

class BinaryLogger:
    def __init__(self):
        self._binary_list = []
        self._statuses = {}
        self._lock = threading.Lock()
        self._binary_colors = {
            "WAITING": Back.YELLOW + Fore.BLACK,
            "DOWNLOADING": Back.BLUE + Fore.WHITE,
            "FINISHED": Back.GREEN + Fore.BLACK
        }
        self._longest = 0
    
    def _print_binary_status(self, binary):
        if binary not in self._binary_list:
            return
        print("\033[K%s%s%s%s" % (Fore.MAGENTA, (binary + ":").ljust(self._longest + 2), self._binary_colors[self._statuses[binary]], (self._statuses[binary])))
    
    def init(self, binary_list):
        self._binary_list = binary_list
        for binary in self._binary_list:
            self._statuses[binary] = "WAITING"
            if len(binary) > self._longest:
                self._longest = len(binary)
        
        for binary in self._binary_list:
            self._print_binary_status(binary)
    
    def update(self, binary):
        if binary not in self._binary_list:
            return
        with self._lock:
            self._statuses[binary] = "DOWNLOADING" if self._statuses[binary] == "WAITING" else "FINISHED"
            print("\033[%dA" % (len(self._binary_list) + 1))
            for binary in self._binary_list:
                self._print_binary_status(binary)

if "--skip-download" not in sys.argv:
    logger = BinaryLogger()
    logger.init(binary_list)
    threads = []

    if not os.path.exists("bin"):
        os.mkdir("bin")

    for binary in binary_list:
        newthread = threading.Thread(target=wait_and_download_thread, args=(binary, "tgrcdev-nightlys", "gdsqlite-native/" + commit + "/bin/", logger))
        newthread.start()
        threads.append(newthread)

    for thread in threads:
        thread.join()
            
else:
    print("Skipped download stage.")

archive_name = "gdsqlite-nightly-%s.zip" % short
if "--skip-zip" not in sys.argv:
    sys.stdout.write("Zipping up files...")
    sys.stdout.flush()

    files = [
        {"path": "LICENSE","arcpath": "lib/gdsqlite/LICENSE"}, {"path": "demo/lib/gdsqlite.gdns", "arcpath":"lib/gdsqlite.gdns"},
        {"path": "bin/gdsqlite.32.dll", "arcpath": "lib/gdsqlite/gdsqlite.32.dll"}, {"path": "bin/gdsqlite.64.dll", "arcpath": "lib/gdsqlite/gdsqlite.64.dll"},
        {"path": "bin/libgdsqlite.32.so", "arcpath": "lib/gdsqlite/libgdsqlite.32.so"}, {"path": "bin/libgdsqlite.64.so", "arcpath": "lib/gdsqlite/libgdsqlite.64.so"},
        {"path": "bin/libgdsqlite.64.dylib", "arcpath": "lib/gdsqlite/libgdsqlite.64.dylib"},
        {"path": "bin/libgdsqlite.armv7.so", "arcpath": "lib/gdsqlite/libgdsqlite.armv7.so"}, {"path": "bin/libgdsqlite.arm64v8.so", "arcpath": "lib/gdsqlite/libgdsqlite.arm64v8.so"},
        {"path": "bin/libgdsqlite.x86.so", "arcpath": "lib/gdsqlite/libgdsqlite.x86.so"}, {"path": "bin/libgdsqlite.x86_64.so", "arcpath": "lib/gdsqlite/libgdsqlite.x86_64.so"},
        {"path": "demo/lib/gdsqlite/library.tres", "arcpath": "lib/gdsqlite/library.tres"}
    ]
    
    archive = zipfile.ZipFile(archive_name, "w", zipfile.ZIP_STORED if "--fat-zip" in sys.argv else zipfile.ZIP_DEFLATED)
    with archive:
        for file in files:
            archive.write(file["path"], file["arcpath"])
    print("Done.")
else:
    print("Skipped zip stage.")

if "--upload" in sys.argv or '-u' in sys.argv:
    class UploadProgress:
        def __init__(self, filename):
            self._filename = filename
            self._size = int(os.path.getsize(filename))
            self._bytes_uploaded = 0
            self._lock = threading.Lock()
            print(" ")
        
        def __call__(self, bytes_amount):
            with self._lock:
                self._bytes_uploaded += bytes_amount
                percent = (self._bytes_uploaded / self._size) * 100
                percent_int = int(percent)
                percent_str = "[" + "".ljust(int(percent_int / 10), '/') + "".ljust(10 - int(percent_int / 10)) + "]"
                print("\033[1A%sUPLOAD PROGRESS: %s%s %f%% %s(%d/%d)" % (Fore.LIGHTRED_EX, Fore.YELLOW, percent_str, percent, Fore.WHITE, self._bytes_uploaded, self._size))

    sys.stdout.write("Beginning upload to S3 bucket tgrcdev-nightlys...")
    sys.stdout.flush()
    bucket.upload_file(archive_name, "gdsqlite-native/" + commit + "/" + archive_name, Callback=UploadProgress(archive_name))
