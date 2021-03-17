# meli-gdrive
Pythonn app for logging Google Drive files in a Redis Data Base.
Also removess Public Files permissions and mantains a historic list of those files

Insstrucctions:

  1. Clone Repository
  2. Go to /app directory and put the credentials.json file. This file contains the keys for using the Gmail and Google Drive        API
    The structure of the file is a JSON like this:
    
    {
    "email_address": "<Email address to be used>",
    "google_client_id": "<Client Id>",
    "google_client_secret": "<Client Secret>",
    "google_refresh_token": ""
    }
  If you don't have one, please refer to this link: 
  https://www.iperiusbackup.net/en/how-to-enable-google-drive-api-and-get-client-credentials/
  
  3. Go to /docker directory
  4. Run docker-compose -f "docker-compose.yml" up -d --build     
  This will build the containers with the api credentials inserted.
  
  5. Run docker exec -it app python main.py       
  This will run the container in intractive mode and authorize the app to make modifications on the user Drive. MUST be done the first time
  
  6. Go to the URL and authorize the app
  7. Paste the authorization code in the terminal
  8. The App will start
  9. If you wish to run app in background Contrl + c to exit app
  10. Run docker exec -d app python main.py
  
In order to view the Data Base run: 
   - docker exec -it app python queryDatabase.py inventario   (To view inventory of User Drive)
   - docker exec -it app python queryDatabase.py publico  (To view historical list of files)
