import os

# Create NameNode if it does not exist
def NameNode(path):
    if not os.path.exists(path):
        with open(path + "/NameNode.json", "w+") as f:
            f.write('{}')

# Create DataNodes if they do not exist
def DataNode(path):
    if os.path.exists(path) == False:
        os.makedirs(path)
        os.makedirs(path + "/DataNode_1")
        os.makedirs(path + "/DataNode_2")