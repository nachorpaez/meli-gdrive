import redis

r = redis.Redis(host='db', port=6379, db=0)
r2 = redis.Redis(host='db',port=6379,db=1)

def getConnection():
      print(r.client_getname())

def listAll():
    keys = r.keys()
    for k in keys:
      print(r.hgetall(k))

def deleteFile(id):
    r.hdel(id,"name","mimeType","modifiedTime","owners","shared")

def getAll(id):
    list = r.hgetall(id)
    for i in list:
        print(i.decode('utf-8') + ":" + list[i].decode('utf-8'))

def listKeys():
    return r.keys()

def listKeys2():
    return r2.keys()

def insertFiles(id, key, value):
    r.hset(id,key,value)

#Insert file in Public database
def insertFilesPublic(id,value):
    r2.set(id,value)

#Insert changes on databse
def insertChanges(id, key, value):
    r.hset(id,key,value)

def getValue2(key):
    return r2.get(key).decode('utf-8')

# keys = listKeys2()
# for k in keys:
#       print(getValue2(k))
# listAll()