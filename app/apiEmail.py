import yagmail

yag = yagmail.SMTP("melichallenge.ar@gmail.com", oauth2_file="./email/email_credentials.json")

def sendEmail(owner, filename):
    yag.send(to=owner, subject="Public Files", 
    contents=("This is an automated message, your Public file " + filename + " has lost it's public permissions. All files must remain private") 
    )