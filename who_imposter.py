import os
import hashlib
import fnmatch
import subprocess

# First: list all the exe files in the AppData/Roaming hidden folder
# Second: hash the exe files found & compare them with the svchost.exe hash (the virus hash)
# Third: if found the delete the exe corresponding to that hash


# hash a file by giving its path
# using tha sha256 algorithm
def hash_function(path):
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


# stop the malicious executable from running by executing a powershell command
# delete the file
def delete_virus(exe_path):
    process = subprocess.Popen(
        ["powershell", "Get-Process | Where-Object { $_.Path -eq '"+exe_path+"' } | ForEach-Object { Stop-Process -Id $_.Id }"], stdout=subprocess.PIPE)
    os.remove(exe_path)


# set up the path of AppData/Roaming hidden folder
Username = os.environ['USERNAME']
folder_path = "C:\Users\{}\AppData\Roaming".format(Username)

# store the virus hash in order to be able to compare it
svchost_hash = hash_function(os.path.join(folder_path, 'svchost.exe'))

# first task


# list all the executables in the AppData/Roaming hidden folder
list_appData_roaming_files = fnmatch.filter(os.listdir(folder_path), "*.exe")
print('Executables list of App/Roaming folder: ')
print(list_appData_roaming_files)


# second task

# run through the files of the list_appData_roaming_files list
# hash each file of it
# compare it with the virus hash
# if a match is found:
# 1- stop the process from running by executing a powershell command
# 2- delete the process

for file in list_appData_roaming_files:
    current_file_path = os.path.join(folder_path, file)
    current_file_hash = hash_function(current_file_path)

    if(current_file_hash == svchost_hash):

        # third task:
        print('-virus found')
        delete_virus(current_file_path)
        print("-virus deleted")
