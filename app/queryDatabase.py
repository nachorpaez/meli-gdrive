import redis
import sys


a = sys.argv[1]

#Print de la base de archivos que fueron publicos
if len(a) != 0:
    if a == "-publico":
        r2 = redis.Redis(host='db',port=6379,db=1)
        keys = r2.keys()
        print("File Name")
        for k in keys:
            print(r2.get(k).decode('utf-8'))
    elif a == "-inventario":
        r = redis.Redis(host='db', port=6379, db=0)
        keys = r.keys()
        print("Name\tFile Type\tOwners\tModified Time\tShared")
        for k in keys:
            file = r.hgetall(k)
            print("{}\t{}\t{}\t{}\t{}".format(
             file['name'.encode('utf-8')].decode('utf-8'),
             file['mimeType'.encode('utf-8')].decode('utf-8'),
             file['owners'.encode('utf-8')].decode('utf-8'),
             file['modifiedTime'.encode('utf-8')].decode('utf-8'),
             file['shared'.encode('utf-8')].decode('utf-8')))
    else:
        print("Error, favor especificar la base de datos Puede ser publico o inventario")
else:
    print("Error, favor especificar la base de datos")