import apiDrive
import apiEmail
import dataBase
import time
import redis

def checkPublicFiles(fileList):
    length = len(fileList["files"])
    for i in range(length):
        id = fileList["files"][i]["id"]
        owner = fileList["files"][i]["owners"]
        fileName = fileList["files"][i]["name"]
        if (fileList["files"][i]["shared"] == "True"): #Si el archivo es Publico procedo a borar los permisos que tiene el archivo
            deletePermissions(id, owner, fileName)
        else:
            for j in fileList["files"][i]:
                if (j !="id"):
                    dataBase.insertFiles(id,j, fileList["files"][i][j]) #Itero por el dict e inserto por id en la base de redis

def checkPublicChanges(changesList):
    length = len(changesList["changes"])
    for i in range(length):
        if changesList["changes"][i]["removed"]:
            dataBase.deleteFile(changesList["changes"][i]["fileId"])
        else:
            fileMetadata = apiDrive.getFileMetadata(changesList["changes"][i]["fileId"])
            fileMetadata["owners"] = fileMetadata["owners"][0]["emailAddress"]
            fileMetadata["mimeType"] = apiDrive.f(fileMetadata["mimeType"])
            fileMetadata["shared"] = str(fileMetadata["shared"])
            id = fileMetadata["id"]
            owner = fileMetadata["owners"]
            fileName = fileMetadata["name"]
            if fileMetadata["shared"] == "True": #Si es Public
                deletePermissions(id, owner, fileName)

            else:
                for j in fileMetadata:
                    if (j !="id"):
                        try:
                            dataBase.insertChanges(id,j, fileMetadata[j])
                        except redis.exceptions.ConnectionError:
                            print("No fue posible conectarse con la base de datos. Favor revisar que el contenedor de Redis este corriendo")
                            exit()

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

    try:
        if not dataBase.listKeys(): #Si no hay keys en la base significa que arranco la app por primera vez entonces me traigo todos los files.
            fileList = apiDrive.getFileList()
            checkPublicFiles(fileList)
            pToken = apiDrive.getStartPageToken() #Pido el primer token para quedar en cero los cambios.
            savePageToken(pToken)
    except redis.exceptions.ConnectionError:
        print("No fue posible conectarse con la base de datos. Favor revisar que el contenedor de Redis este corriendo")
        exit()

    if pToken == None:
        #pToken no tiene valor, por lo tanto tomo el ultimo guardado en archivo
        pToken = getPageToken()  

    while(not time.sleep(5)): 
    #     #Pido traer la lista de cambios con el token mas actual que tengo
        tuple = apiDrive.getChangesList(pToken)

        #La funcion me devuelve el nuevo token que esta sin cambios pendientes y la lista de cambios que hubo
        pToken = tuple[1]
        savePageToken(str(pToken))
        changesList = tuple[0]
        if changesList["changes"]:
            checkPublicChanges(changesList)


