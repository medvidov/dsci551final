import client
import subprocess
import asyncio
import json
import utils
import commands
import nodes

# Runs the main server and UI
if __name__ == "__main__":

    nodes.DataNode("nodes")
    nodes.NameNode("nodes")
    
    # Open the server per assignment requirements
    p = subprocess.Popen(["python", "server.py"])

    while True:
        user_input = input('edfs$ ')
        split_input = user_input.split(' ')
        command = split_input[0]

        if command == 'ls':
            asyncio.run(client.tcp_client(commands.ls(split_input[1])))

        if command == 'rm':
            asyncio.run(client.tcp_client(commands.rm(split_input[1])))

        if command == 'put':
            asyncio.run(client.tcp_client(commands.put(split_input[1], split_input[2])))

        if command == 'get':
            asyncio.run(client.tcp_client(commands.get(split_input[1], split_input[2])))

        if command == 'mkdir':
            asyncio.run(client.tcp_client(commands.mkdir(split_input[1])))

        if command == 'rmdir':
            asyncio.run(client.tcp_client(commands.rmdir(split_input[1])))

        if command == 'cat':
            asyncio.run(client.tcp_client(commands.cat(split_input[1])))

        if user_input == 'quit':
            exit()  
