import shutil
import socket
import os
import re

dir = os.path.join(os.getcwd(), 'test')

def process(req):
    global dirname
    if req == 'pwd':
        return dir
    elif req == 'lst':
        return '; '.join(os.listdir(dir))
    elif req[:3] == 'crt':
        newpath = '/'.join([dir, re.search(r"<([A-Za-z0-9_]+)>", req).group(1)])
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            os.chdir(newpath)
            dir = os.getcwd()
            return f"{newpath} directory created successfully"
        else:
            return f"Directory with a such name is already exists"
    elif req[:3] == 'crf':
        file_name = re.search(r"<([A-Za-z0-9_]+\.+[t]+[x]+[t]+)>", req).group(1)
        info = re.search(r"\[([A-Za-z0-9_]+)\]", req).group(1)
        if not os.path.exists('/'.join([dir, file_name])):
            text_file = open('/'.join([dir, file_name]), "w")
            text_file.write(info)
            text_file.close()
            return f"File {file_name} created successfully"
        else:
            return f"File with a such name is already exists"
    elif req[:3] == 'rem':
        mydir = '/'.join([dir, re.search(r"<([A-Za-z0-9_]+)>", req).group(1)])
        print(mydir)
        if  os.path.exists(mydir):
            shutil.rmtree(mydir)
            return f"{mydir} deleted successfully!"
        else:
            return f"Failed search"
    elif req[:3] == 'ref':
        filename = '/'.join([dir, re.search(r"<([A-Za-z0-9_]+\.+[t]+[x]+[t]+)>", req).group(1)])
        if os.path.exists(filename):
            os.remove(filename)
            return f"File  was deleted successfully!"
        else:
            return f"Failed search"

    elif req[:3] == 'ren':
        filename = '/'.join([dir, re.search(r"<([A-Za-z0-9_]+\.+[t]+[x]+[t]+)>", req).group(1)])
        new_file_name = '/'.join([dir, re.search(r"\[([A-Za-z0-9_] + \.+[t]+[x]+[t]+)\]", req).group(1)])
        print(filename)
        if os.path.exists(filename):
            os.rename(filename, new_file_name)
            return f"File was renamed successfully!"
        else:
            return f"Failed search"
    elif req == 'cup':
        os.chdir('../')
        return f"Now you are in {os.getcwd()}"

    elif req[:3] == 'chd':
        path = '/'.join([dir, re.search(r"<([A-Za-z0-9_]+)>", req).group(1)])
        if os.path.exists(path):
            os.chdir(path)
            return f"Now you are in {os.getcwd()}"
        else:
            return "Failed search!"
    elif req[:3] == 'get':
        filename = '/'.join([dir, re.search(r"<([A-Za-z0-9_]+\.+[t]+[x]+[t]+)>", req).group(1)])
        f = open(filename, mode='r', encoding='utf-8')
        text = f.read()
        print(text)
        return f"{text}"
    return 'bad request'


PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:
    conn, addr = sock.accept()

    request = conn.recv(1024).decode()
    print(request)

    response = process(request)
    conn.send(response.encode())

    conn.close()
