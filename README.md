# meli-gdrive

App para loguear inventario de archivos de Google Drive.
Remueve permisos de archivos publicos y mantiene un historico de estos archivos.

Para utilizar la app:

  1- Clone Repository
  2- Go to /app directory and put the credentials.json file. This file contains the keys for using the Gmail and Google Drive        API
    The structure of the file is a JSON like this:
    {
    "email_address": "<Email address to be used>",
    "google_client_id": "<Client Id>",
    "google_client_secret": "<Client Secret>",
    "google_refresh_token": ""
    }
  3- Go to /docker directory
  4- Run docker-compose -f "docker-compose.yml" up -d --build     This will build the containers with the api credentials inserted.
  5- Run docker exec -it app python main.py       This will run the container and authorize the app to make modifications on the user Drive. MUST be done the first time
  6- Go to the URL and authorize the app
  7- Paste the authorization code in the terminal
  8- The App will start
  9- If you wish to run app in background Contrl + c to exit app
    9.1- Run docker exec -d app python main.py
  
In order to view the Data Base run: 
      docker exec -it app python queryDatabase.py -inventario   (To view inventory of User Drive)
      docker exec -it app python queryDatabase.py -publico  (To view historical list of files)
