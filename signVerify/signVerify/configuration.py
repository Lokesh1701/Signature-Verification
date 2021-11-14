import hashlib
import os

def getFileSize(filePath):
    file_size = os.path.getsize(filePath)
    size = str(round(file_size / (1024 * 1024), 3)) + "MB"
    return size

def getFolderSize(filePath):
    original_folder_size = 0
    for path, dirs, files in os.walk(filePath):
        for f in files:
            fp = os.path.join(path, f)
            original_folder_size += os.path.getsize(fp)
    return str(round(original_folder_size / (1024 * 1024), 3)) + "MB"

def getChecksum(filePath):
    md5_hash = hashlib.md5()
    a_file = open(filePath, "rb")
    content = a_file.read()
    md5_hash.update(content)
    digest = md5_hash.hexdigest()
    return digest