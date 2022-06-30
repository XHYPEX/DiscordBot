# importing the requests module
import requests

print('Downloading started')
url = 'https://mirror0.maidservant.org/file/nostrike/2d7fe7b8d3a10b8f95c994ead8926c79/Trap_Legend_Patch.zip'

# Downloading the file by sending the request to the URL
req = requests.get(url)

# Split URL to get the file name
filename = url.split('/')[-1]

# Writing the file to the local file system
with open(filename, 'wb') as output_file:
    output_file.write(req.content)
print('Downloading Completed')