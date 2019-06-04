import apiDrive
import apiEmail
import dataBase
import time
import redis

#Function checks if file is Shared, if it is it calles the deletePermissions function, else it inserts the file in the db
def checkPublicFiles(fileList):
    length = len(fileList["files"])
    for i in range(length):
        id = fileList["files"][i]["id"]
        owner = fileList["files"][i]["owners"]
        fileName = fileList["files"][i]["name"]
        if (fileList["files"][i]["shared"] == "True"):
            deletePermissions(id, owner, fileName)
        else:
            for j in fileList["files"][i]:
                if (j !="id"):
                    dataBase.insertFiles(id,j, fileList["files"][i][j])

#Function checks if the file was removed, else it checks if the file is shared. In that case it calles the delete permissions
#function. Else it inserts the file in the db
def checkPublicChanges(changesList):
    length = len(changesList["changes"])
    for i in range(length):
        if changesList["changes"][i]["removed"]:
            dataBase.deleteFile(changesList["changes"][i]["fileId"])
        else:
            #Since the changesList only has the file Id, I need to get the file metadata
            fileMetadata = apiDrive.getFileMetadata(changesList["changes"][i]["fileId"])
            fileMetadata["owners"] = fileMetadata["owners"][0]["emailAddress"]
            #Convert name of file type
            fileMetadata["mimeType"] = apiDrive.f(fileMetadata["mimeType"])
            fileMetadata["shared"] = str(fileMetadata["shared"])
            id = fileMetadata["id"]
            owner = fileMetadata["owners"]
            fileName = fileMetadata["name"]
            if fileMetadata["shared"] == "True": #If it is Shared
                deletePermissions(id, owner, fileName)
            else:
                for j in fileMetadata:
                    if (j !="id"):
                        try:
                            dataBase.insertChanges(id,j, fileMetadata[j])
                        except redis.exceptions.ConnectionError:
                            print("No fue posible conectarse con la base de datos. Favor revisar que el contenedor de Redis este corriendo")
                            exit()

#With the file id the function deletes all the permissions of the file.
def deletePermissions(id, owner, fileName):
    # File is shared so I get the permissions list
    permissionsList = apiDrive.listPermissions(id)
    length2 = len(permissionsList["permissions"])
    for k in range(length2): #Iterate througth the list of permissions
        if permissionsList["permissions"][k]["role"] != "owner":
            apiDrive.removePermissions(id, permissionsList["permissions"][k]["id"])
            apiEmail.sendEmail(owner,fileName)
            try:
                dataBase.insertFilesPublic(id,fileName)    
            except redis.exceptions.ConnectionError:
                print("No fue posible conectarse con la base de datos. Favor revisar que el contenedor de Redis este corriendo")
                exit()

#To mantain the token through the app restart I need to save it to a file
def savePageToken(pToken):
    TOKENS = 'start_page_token.txt'
    token_file = open(TOKENS,'w')
    token_file.write(pToken)
    token_file.close()

def getPageToken():
    TOKENS = 'start_page_token.txt'
    token_file = open(TOKENS)
    pToken = token_file.read()
    token_file.close()
    return pToken

if __name__ == '__main__':
    pToken = None
    print("Script started")
    try:
        #If there are no keys on the database it means there are no changes to check so I get all files
        if not dataBase.listKeys():
            fileList = apiDrive.getFileList()
            checkPublicFiles(fileList)
            pToken = apiDrive.getStartPageToken()
            savePageToken(pToken)
    except redis.exceptions.ConnectionError:
        print("No fue posible conectarse con la base de datos. Favor revisar que el contenedor de Redis este corriendo")
        exit()

    if pToken == None:
        #Token has no value so I get the last saved one
        pToken = getPageToken()  

    while(not time.sleep(5)): 
        #Get the list of changes more recent
        tuple = apiDrive.getChangesList(pToken)

        #Function returns the list of changes and the next token
        pToken = tuple[1]
        savePageToken(str(pToken))
        changesList = tuple[0]
        if changesList["changes"]:
            checkPublicChanges(changesList)


