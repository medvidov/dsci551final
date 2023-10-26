import os
import json

# Check if EDFS path exists
def edfs_exists(path):

    # The root directory automatically exists
    if path != '/':
        f = open('nodes/NameNode.json')
        files = json.load(f)
        
        chunks = path.split('/')

        # Ignore the first, empty chunk of the path
        for i in chunks[1:]:
            if i in files.keys():
                files = files[i]
            else:
                return False

    return True

# Check if local path exists
def local_exists(path):

    if os.path.exists(path):
        return True
    
    return False

# Get file size
def get_local_size(path):
    return os.path.getsize(path)

# Check if local path is to a folder
def local_folder(path):
    return os.path.isdir(path)

# Check if EDFS path is to a folder
def edfs_folder(path):

    if '.' not in path:
        return True
    else:
        return False