Team members: Pavle Medvidovic

Project topic: Emulating HDFS (EDFS). I have opted to use a subset of the Amazon Review dataset as  my sample data because I just need KBs and MBs (and even GBs) of data. The contents do not matter as much as the size of the files.

I have included sample data and my NameNode and DataNode in this submission to aid in running this code. However, if you wanted to run the code from scratch, you would simply run `python edfs.py` and all necessary files and directories would be created for you.

Command Usage (note that all EDFS paths MUST include a leading '/'):

ls </path>

rm </path to EDFS file>

put <path to local file> </existing path to EDFS file>

mkdir </path to target EDFS directory>

rmdir </path to empty EDFS directory>

cat </path to file to print>

get </existing path to EDFS file> <path to local file OR target directory>

Source Code:
client.py
commands.py
edfs.py
nodes.py
server.py
utils.py
testing.ipynb (used to test code when I needed additional output)
