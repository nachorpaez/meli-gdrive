import httplib2
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from apiclient.discovery import build
import json


with open("credentials.json", "r") as read_file:
    data = json.load(read_file)
    client_id = data["google_client_id"]
    client_secret = data["google_client_secret"]

# The scope URL for read/write access to a user's drive data
scope = 'https://www.googleapis.com/auth/drive'

# Create a flow object. This object holds the client_id, client_secret, and
# scope. It assists with OAuth 2.0 steps to get user authorization and
# credentials.
flow = OAuth2WebServerFlow(client_id, client_secret, scope)

# Create a Storage object. This object holds the credentials that your
# application needs to authorize access to the user's data. The name of the
# credentials file is provided. If the file does not exist, it is
# created. This object can only hold credentials for a single user, so
# as-written, this script can only handle a single user.
storage = Storage('credentials.dat')

# The get() function returns the credentials for the Storage object. If no
# credentials were found, None is returned.
credentials = storage.get()

# If no credentials are found or the credentials are invalid due to
# expiration, new credentials need to be obtained from the authorization
# server. The oauth2client.tools.run_flow() function attempts to open an
# authorization server page in your default web browser. The server
# asks the user to grant your application access to the user's data.
# If the user grants access, the run_flow() function returns new credentials.
# The new credentials are also stored in the supplied Storage object,
# which updates the credentials.dat file.
if credentials is None or credentials.invalid:
    flags = ['--noauth_local_webserver']
    credentials = tools.run_flow(flow, storage, tools.argparser.parse_args(flags))

# Create an httplib2.Http object to handle our HTTP requests, and authorize it
# using the credentials.authorize() function.
http = httplib2.Http()
http = credentials.authorize(http)

# The apiclient.discovery.build() function returns an instance of an API service
# object can be used to make API calls. The object is constructed with
# methods specific to the drive API. The arguments provided are:
#   name of the API ('drive')
#   version of the API you are using ('v3')
#   authorized httplib2.Http() object that can be used for API calls
service = build('drive', 'v3', http=http)

#Function to convert mimeType strings
def f(x):
        return{
          "application/vnd.google-apps.spreadsheet":"Google Spreadsheet",
          "application/vnd.google-apps.document":"Google Document",
          "application/vnd.google-apps.jam":"Google Jam",
          "application/vnd.google-apps.site":"Google Site",
          "application/vnd.google-apps.map":"Goole Map",
          "application/vnd.google-apps.form":"Google Form",
          "application/vnd.google-apps.presentation":"Google Presentation",
          "application/vnd.google-apps.folder":"Folder",
          "application/vnd.google-apps.drawing":"Google Draw"

        }.get(x,x)

#Get list of files in the user Drive
def getFileList():
  request = service.files().list(
      corpora="user",
      fields="files(id,name,mimeType,owners(emailAddress),shared,modifiedTime)"
    )
  response = request.execute()
  length = len(response["files"])
  for i in range(length):
      response["files"][i]["owners"] = response["files"][i]["owners"][0]["emailAddress"]
      response["files"][i]["mimeType"] = f(response["files"][i]["mimeType"])
      #Boolean shared is transformed to string in order to insert it in Redis DB
      response["files"][i]["shared"] = str(response["files"][i]["shared"])
  return response

def getFileMetadata(fileId):
  request = service.files().get(fileId=fileId,fields="id,name,mimeType,owners(emailAddress),shared,modifiedTime")
  response = request.execute()
  return response

#Get the list of changes since the last start page token requested
def getChangesList(pToken):
  request = service.changes().list(pageToken=pToken,restrictToMyDrive=True,fields="newStartPageToken,changes(removed,fileId)")
  response = request.execute()
  if "newStartPageToken" in response:
    pToken = response["newStartPageToken"]
  return response, pToken

def getStartPageToken():
  request = service.changes().getStartPageToken(fields="startPageToken")
  response = request.execute()
  return response["startPageToken"]

def listPermissions(fileId):
  request = service.permissions().list(fileId=fileId,fields="permissions(id,role)")
  response = request.execute()
  return response
  
def removePermissions(fileId, permissionId):
  request = service.permissions().delete(fileId=fileId, permissionId=permissionId)
  request.execute()



