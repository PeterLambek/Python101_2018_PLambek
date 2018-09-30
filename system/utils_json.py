import maya.cmds as maya
import json
import tempfile

#save file data
def writeJson(fileName, data):
    #save the file with wright mode 'w', saving it as outfile
    with open(fileName, 'w') as outfile:
        #dunp json.dump the data that we are passing in as an argument to the outfile
        json.dump(data, outfile)
    #and then close the file
    file.close(outfile)

#open a file
def readJson(fileName):
    #open the file with read mode 'r', saving it as infile
    with open(fileName, 'r') as infile:
        #data will be equal to the read file
        data = (open(infile.name, 'r').read())
    #the return the data for what ever function that is calling for it
    return data
