FROM python:3

RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client mysql-connector-python yagmail redis

WORKDIR /app

RUN touch /app/start_page_token.txt

ADD /app .