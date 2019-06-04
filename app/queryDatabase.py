import redis
import sys

if len(sys.argv[1]) > 0:
    a = sys.argv[1]
    #Print of data base of historic public files
    if a == "-publico":
        r2 = redis.Redis(host='db',port=6379,db=1)
        keys = r2.keys()
        print("File Name")
        for k in keys:
            print(r2.get(k).decode('utf-8'))
    elif a == "-inventario":
        #Print of actual inventory of files
        r = redis.Redis(host='db', port=6379, db=0)
        keys = r.keys()
        print("Name\t\tFile Type\tOwners\t\t\tModified Time\tShared")
        for k in keys:
            file = r.hgetall(k)
            print("{}\t\t{}\t{}\t\t\t{}\t{}".format(
             file['name'.encode('utf-8')].decode('utf-8'),
             file['mimeType'.encode('utf-8')].decode('utf-8'),
             file['owners'.encode('utf-8')].decode('utf-8'),
             file['modifiedTime'.encode('utf-8')].decode('utf-8'),
             file['shared'.encode('utf-8')].decode('utf-8')))
    else:
        print("Error, favor especificar la base de datos Puede ser publico o inventario")
else:
    print("Error, favor especificar la base de datos")