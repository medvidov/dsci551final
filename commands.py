import utils
import json
import uuid
import shutil
import math
import os

max_block_size = 134217728

# ls
def ls(path):
    
    if path[0] != '/':
        return 'Invalid path. Proper usage is ls </path>.'
    
    stuff = ''
    
    # If we are in a path and a folder
    if utils.edfs_exists(path):
        if utils.edfs_folder(path):

            # If we are not in root, traverse the JSON and print the files
            if path != '/':
                f = open('nodes/NameNode.json')
                files = json.load(f)
                chunks = path.split('/')
                for i in chunks[1:]:
                    files = files[i]
                for j in files:
                    stuff =  stuff + j + ' '
                return stuff.strip()
            
            # If we are in root, simply print the files
            if path == '/':
                f = open('nodes/NameNode.json')
                files = json.load(f)
                for i in files.keys():
                    stuff = stuff + i + ' '
                return stuff.strip()
        else:
            return 'The specified path does not point to a directory on EDFS.'
    else:
        return 'The specified path does not point to a directory on EDFS.'
        
    return

# rm
def rm(path):

    if path[0] != '/':
        return 'Invalid path. Proper usage is rm </path to file>.'
    
    # Ensure the path exists and that we do not point to a folder
    if utils.edfs_exists(path):
        if not utils.edfs_folder(path):
            f = open('nodes/NameNode.json')
            files = json.load(f)
            new_files = files
            
            chunks = path.split('/')
            
            # Find the file and delete the data from DataNodes
            for i in chunks[1:]:
                if len(chunks) > 2:
                    files = files[i]
                    if i == chunks[len(chunks) - 2]:
                        for j in files[chunks[len(chunks) - 1]]:
                            if os.path.exists('nodes/DataNode_1/' + j[0]):
                                os.remove('nodes/DataNode_1/' + j[0])
                            if os.path.exists('nodes/DataNode_2/' + j[0]):
                                os.remove('nodes/DataNode_2/' + j[0])
                        del files[chunks[len(chunks) - 1]]
                        break
                # Similar process if we're in root
                else:
                    for j in files[chunks[len(chunks) - 1]]:
                        if os.path.exists('nodes/DataNode_1/' + j[0]):
                            os.remove('nodes/DataNode_1/' + j[0])
                        if os.path.exists('nodes/DataNode_2/' + j[0]):
                            os.remove('nodes/DataNode_2/' + j[0])
                    del files[chunks[len(chunks) - 1]]
                    break

            # Update the JSON
            if len(chunks) > 2:
                for i in chunks[1:]:
                    if i == chunks[len(chunks) - 2]:
                        new_files[i] = files
            else:
                new_files = files
            
            with open("nodes/NameNode.json", "w") as outfile:
                json.dump(new_files, outfile, indent = 4)
                
            return 'Successfully deleted {}.'.format(path)
        else:
            return 'The specified path does not point to a file on EDFS.'
    else:
        return 'The specified path does not point to a file on EDFS.'
    
    return

# put
def put(local_path, edfs_path):
    
    path_to_file = edfs_path.rsplit('/', 1)[0]
    file_name = edfs_path.rsplit('/', 1)[1]
    
    # Check for every possible combo of paths that might mess up put
    if not utils.local_exists(local_path):
        return 'The specified path on the local machine does not exist.'
    
    if utils.edfs_exists(edfs_path):
        return 'Invalid path. {} already exists.'.format(edfs_path)
    
    if not utils.edfs_exists(path_to_file):
        return 'Invalid path. {} does not exist, so no file can be put there.'.format(edfs_path)
    
    if utils.edfs_folder(edfs_path):
        return 'Invalid path. {} does not specify a file.'.format(edfs_path)
    
    if utils.local_folder(local_path):
        return 'Invalid path. {} does not specify a file.'.format(local_path)
    
    if edfs_path[0] != '/':
        return 'Invalid path. Proper usage is put <path to local file> </existing path to EDFS file>.'
    
    # If both paths exist and we have no issues with paths
    if utils.local_exists(local_path) and utils.edfs_exists(path_to_file):
        f = open('nodes/NameNode.json')
        files = json.load(f)
        new_files = files

        # If we are working in root, we can essentially just put the file in
        # There are some quirks based on the size of the file
        if path_to_file == '':

            # Get the size
            size = utils.get_local_size(local_path)
            if(size < 1000):
                size = str(size)+ ' B'
            else:
                sizes = ['B', 'KB', 'MB', 'GB', 'TB']
                prefix = int(math.floor(math.log(size, 1000)))
                magnitude = math.pow(1000, prefix)
                rounded = round(size/magnitude, 2)
                size = str(rounded) + ' ' + sizes[prefix]
            
            blocks = []
            file_type = local_path.split('.')[1]
            file_breakdown = []
            
            # If we are larger than the maximum block size we split the file
            if utils.get_local_size(local_path) > max_block_size:
                os.makedirs('nodes/tmp')
                
                with open(local_path) as f:
                    chunk = f.read(max_block_size)
                    while chunk:
                        uid = str(uuid.uuid4())
                        with open('nodes/tmp/' + uid + '.' + file_type, 'w+') as chunk_file:
                            chunk_file.write(chunk)
                        file_breakdown.append(uid + '.' + file_type)
                        chunk = f.read(max_block_size)
                f.close()
                
                
                for file_chunk in file_breakdown:
                    blocks.append([file_chunk, '1', '2'])
                    shutil.copyfile('nodes/tmp/' + file_chunk, 'nodes/DataNode_1/' + file_chunk)
                    shutil.copyfile('nodes/tmp/' + file_chunk, 'nodes/DataNode_2/' + file_chunk)
                    
                blocks.append([size])
                
                new_files[file_name] =  blocks
                        
                shutil.rmtree('nodes/tmp')
             
            # This process is essentially repeated with extra processing for being outside of root
            else:
                uid = str(uuid.uuid4())
                os.makedirs('nodes/tmp')
                with open(local_path) as f:
                    with open('nodes/tmp/' + uid + '.' + file_type, 'w+') as tmp_file:
                        tmp_file.write(f.read())
                    file_breakdown.append(uid + '.' + file_type)
                f.close()
                
                for file_chunk in file_breakdown:
                    blocks.append([file_chunk, '1', '2'])
                    shutil.copyfile('nodes/tmp/' + file_chunk, 'nodes/DataNode_1/' + file_chunk)
                    shutil.copyfile('nodes/tmp/' + file_chunk, 'nodes/DataNode_2/' + file_chunk)
                    
                blocks.append([size])
                
                new_files[file_name] =  blocks
                        
                shutil.rmtree('nodes/tmp')
                
        else:
                    
            size = utils.get_local_size(local_path)
            if(size < 1000):
                size = str(size)+ ' B'
            else:
                sizes = ['B', 'KB', 'MB', 'GB', 'TB']
                prefix = int(math.floor(math.log(size, 1000)))
                magnitude = math.pow(1000, prefix)
                rounded = round(size/magnitude, 2)
                size = str(rounded) + ' ' + sizes[prefix]
            
            blocks = []
            file_type = local_path.split('.')[1]
            file_breakdown = []
            
            if utils.get_local_size(local_path) > max_block_size:
                os.makedirs('nodes/tmp')
                
                with open(local_path) as f:
                    chunk = f.read(max_block_size)
                    while chunk:
                        uid = str(uuid.uuid4())
                        with open('nodes/tmp/' + uid + '.' + file_type, 'w+') as chunk_file:
                            chunk_file.write(chunk)
                        file_breakdown.append(uid + '.' + file_type)
                        chunk = f.read(max_block_size)
                f.close()
                
                
                for file_chunk in file_breakdown:
                    blocks.append([file_chunk, '1', '2'])
                    shutil.copyfile('nodes/tmp/' + file_chunk, 'nodes/DataNode_1/' + file_chunk)
                    shutil.copyfile('nodes/tmp/' + file_chunk, 'nodes/DataNode_2/' + file_chunk)
                    
                blocks.append([size])
                
                chunks = path_to_file.split('/')
            
                for i in chunks[1:]:
                    files = files[i]

                files[file_name] = blocks

                for i in chunks[1:]:
                    if i == chunks[len(chunks) - 1]:
                        new_files[i][file_name] = blocks
                        
                shutil.rmtree('nodes/tmp')
                
            else:
                uid = str(uuid.uuid4())
                os.makedirs('nodes/tmp')
                with open(local_path) as f:
                    with open('nodes/tmp/' + uid + '.' + file_type, 'w+') as tmp_file:
                        tmp_file.write(f.read())
                    file_breakdown.append(uid + '.' + file_type)
                f.close()
                
                for file_chunk in file_breakdown:
                    blocks.append([file_chunk, '1', '2'])
                    shutil.copyfile('nodes/tmp/' + file_chunk, 'nodes/DataNode_1/' + file_chunk)
                    shutil.copyfile('nodes/tmp/' + file_chunk, 'nodes/DataNode_2/' + file_chunk)
                    
                blocks.append([size])
                
                chunks = path_to_file.split('/')
            
                for i in chunks[1:]:
                    files = files[i]

                files[file_name] = blocks

                for i in chunks[1:]:
                    if i == chunks[len(chunks) - 1]:
                        new_files[i][file_name] = blocks
                        
                shutil.rmtree('nodes/tmp')
                                    
        with open("nodes/NameNode.json", "w") as outfile:
            json.dump(new_files, outfile, indent = 4)

        return 'Successfully created {}.'.format(edfs_path)
    

# mkdir
def mkdir(path):

    # Ensure that the path is valid
    if path[0] != '/':
        return 'Invalid path. Proper usage is mkdir </path to target directory>.'
    
    if path == '/':
        return 'Invalid path. Root (/) cannot be recreated.'
    
    if '.' in path:
        return 'Directory names cannot contain periods.'
    
    if utils.edfs_exists(path):
        return 'Invalid path. {} already exists.'.format(path)
    
    # Find the place where we want to insert the directory
    else:
        
        path_to_dir = path.rsplit('/', 1)[0]
        dir_name = path.rsplit('/', 1)[1]
        
        if utils.edfs_exists(path_to_dir):
            f = open('nodes/NameNode.json')
            files = json.load(f)
            new_files = files
                        
            # If it's in root we can just make it
            if path_to_dir == '':
                new_files[dir_name] = {}
            else:

                # Otherwise we iterate through the JSON until we find the location
                chunks = path_to_dir.split('/')

                for i in chunks[1:]:
                    files = files[i]

                files[dir_name] = {}
            
            with open("nodes/NameNode.json", "w") as outfile:
                json.dump(new_files, outfile, indent = 4)
                
            return 'Successfully created {}.'.format(path)
        else:
            return 'Invalid path. The path to the directory you are trying to create does not exist.'
        
    return

# rmdir
def rmdir(path):

    # Ensure that the path is valid
    if path[0] != '/':
        return 'Invalid path. Proper usage is rmdir </path to empty directory>.'
    
    if path == '/':
        return 'Invalid path. Root (/) cannot be deleted.'
    
    if utils.edfs_exists(path):
        if utils.edfs_folder(path):
            
            f = open('nodes/NameNode.json')
            files = json.load(f)
            new_files = files
            
            chunks = path.split('/')
            
            for i in chunks[1:]:
                files = files[i]
            
            if len(files) > 0:
                return 'The directory must be empty to use rmdir.'
            
            # Given an empty directory we iterate through the JSON and delete the correct directory
            else:
                if len(chunks) > 2:
                    for i in chunks[1:]:
                        if i == chunks[len(chunks) - 2]:
                            del new_files[chunks[len(chunks) - 2]][chunks[len(chunks) - 1]]
                            break
                else:
                    # There is some math involved in the event that we are note deleting a directory in root
                    del new_files[chunks[1]]
                        
            with open("nodes/NameNode.json", "w") as outfile:
                json.dump(new_files, outfile, indent = 4)
                
            return 'Successfully deleted {}.'.format(path)
        else:
            return 'The specified path does not point to a directory on EDFS.'
    else:
        return 'The specified path does not point to a directory on EDFS.'
    
    return

# cat   
def cat(path):
    
    # Parse path to ensure file exists and can be printed
    if path[0] != '/':
        return 'Invalid path. Proper usage is cat </path to EDFS file to print>.'
    
    if not utils.edfs_exists(path):
        return '{} cannot be printed because it does not exist.'.format(path)
    else:
        if utils.edfs_folder(path):
            return '{} cannot be printed because it is not a file.'.format(path)
        
        # If we can print the file, we open the relevant DatNodes and just read the content
        else:
            f = open('nodes/NameNode.json')
            files = json.load(f)

            chunks = path.split('/')

            # Ignore the first, empty chunk of the path
            for i in chunks[1:]:
                if i in files.keys():
                    files = files[i]

            content = ''
            for j in files:
                with open('nodes/DataNode_1/' + files[0][0]) as f1:
                    content = f1.read().strip()
                    
        return content

# get
def get(edfs_path, local_path):
    
    path_to_file = local_path.rsplit('/', 1)[0]
    
    # Parse paths to ensure both files exist
    if edfs_path[0] != '/':
        return 'Invalid path. Proper usage is get </existing path to EDFS file> <path to local file OR target directory>.'
    
    if utils.edfs_folder(edfs_path):
        return 'Invalid path. {} does not specify a file.'.format(edfs_path)
    
    if not utils.edfs_exists(edfs_path):
        return 'Invalid path. {} does not exist.'.format(edfs_path)
    
    if '/' in path_to_file and not utils.local_exists(path_to_file):
        return 'The specified local path does not exist.'
    
    # Use cat to directly write content to file
    content = cat(edfs_path)
    with open(local_path, 'w') as f:
        f.write(content)
        
    return 'Successfully wrote {} to {}.'.format(edfs_path, local_path)