import json
import requests
from base64 import b64encode, b64decode
from urllib.parse import urlparse, parse_qsl, urlencode, quote_plus
import urllib, random
import time

f_bug = open("/root/sync/bug.txt").read().split("\n")
main_config = json.loads(open("/root/sync/config.json","r").read())

bugs = [i for i in f_bug if i]
#CONFIG PRIVATE KEY
private_key = main_config["private_key"]
#######################
#config file output
config_public = main_config["file_public"]
config_private = main_config["file_private"]
#######################
#config main
pathdir = "/etc/openclash/proxy_provider/"
time_loop = main_config["time_loop"]
mode_ = main_config["mode_"] # untuk mode bisa di rubah ke ssl atau proxy
#######################
#config untuk mode proxy
try:
    proxy = open("proxy", "r").read()
except:
    proxy = ""
sni = bugs[0]
#######################
#config server DB
serverDB = "http://botwa.fastxd.com"
portDB = "2022"
######################
private_status = True
data_private_old = {}
data_public_old = {}

print("STARTING...")

def getInfo():
    info = "========================= INFO ==========================\n"
    info += "\nBUGS :  "+ str(bugs)
    info += "\nMODE :  " + mode_
    info += "\nPRIVATE KEY :  "+ private_key
    info += "\nPUBLIC FILE :  "+ str(config_public)
    info += "\nPRIVATE FILE :  "+ str(config_private)
    info += "\n\n============== AUTO SYNC BY : OPREKER TEAM ===============\n"
    return info

def decode(data):
    data = b64decode(data)
    return data.decode('utf-8')

def encode(msg):
    msg_bytes = msg.encode('utf-8')
    base64_bytes = b64encode(msg_bytes)
    return base64_bytes.decode('utf-8')


def convert(vmess, reverse="false"):
    vmess = quote_plus(vmess)
    r =requests.get(f"https://sub.bonds.id/sub2?target=clash&url={vmess}&insert=false&config=base%2Fdatabase%2Fconfig%2Fstandard%2Fstandard_redir.ini&emoji=false&list=true&udp=true&tfo={reverse}&expand=false&scv=true&fdn=false&sort=false&new_name=true", timeout=5)
    return r.text
    
def savePublicAcount(config):
    for i in config_public:
        open(pathdir+i, "w").write(config)
        print("UPDATE : "+pathdir+i)
        
def savePrivateAcount(config):
    for i in config_private:
        open(pathdir+i, "w").write(config)
        print("UPDATE : "+pathdir+i)

def parseVmess(data):
    a = data.replace("vmess://", "")
    obj = json.loads(decode(a))
    bug = random.choice(bugs)
    if mode_ == "ws":
        obj["add"] = bug
    if mode_ == "ssl":
        obj["add"] = obj["host"]
        obj["host"] = bug
        obj["sni"] = bug
    if mode_ == "proxy":
       obj["add"] = proxy
       obj["sni"] = sni
       obj["path"] = f"ws://{sni}{obj['path']}"
       
    return "vmess://"+encode(json.dumps(obj))

def parseUrl(urls):
    bug = random.choice(bugs)
    url = urlparse(urls)
    net = url.netloc.split("@")
    id = net[0]
    host = net[1].split(":")[0]
    port = net[1].split(":")[1]
    q = dict(parse_qsl(url.query))
    
    if mode_ == "ws":
        query = urlencode(q)
        urls = f"{url.scheme}://{id}@{bug}:{port}?{query}#{url.fragment}"
    if mode_ == "ssl":
        if "type" not in q:
            q["type"] = "tcp"
        if q["type"] == "grpc":
            hosts = q["host"]
        if q["type"] == "tcp":
            hosts = q["sni"]
        if q["type"] == "ws":
            hosts = q["host"]
        q["sni"] = bug
        q["host"] = bug
        query = urlencode(q)
        urls = f"{url.scheme}://{id}@{hosts}:{port}?{query}#{url.fragment}"
    if mode_ == "proxy":
        path = f'wss://{sni}{q["path"]}'
        q["path"]= path
        q["sni"] = sni
        query = urlencode(q)
        urls = f"{url.scheme}://{id}@{proxy}:{port}?{query}#{url.fragment}"
    return urls
    
def private_proses():
    r = requests.get(f"{serverDB}:{portDB}/private?key={private_key}", timeout=5)
    if r.status_code == 200:
        data = r.json()
        acount = ""
        for k, val in data.items():
            if "vmess://" in val:
                res = parseVmess(val)
                acount += res+"|"
            else:
                res = parseUrl(val)
                acount += res+"|"
        return data, acount

def public_proses():
    r = requests.get(f"{serverDB}:{portDB}/api", timeout=5)
    if r.status_code == 200:
        data = r.json()
        acount = ""
        for k, val in data.items():
            if "vmess://" in val:
                res = parseVmess(val)
                acount += res+"|"
            else:
                res = parseUrl(val)
                acount += res+"|"
        return data, acount
 
if __name__ == "__main__":
    print(getInfo())
    no = 0
    while True:
        time.sleep(time_loop)
        try:
            dataPub = public_proses()
            if private_status:
                dataz = private_proses()
                if dataz:
                    if dataz[0] != data_private_old:
                        data_private_old = dataz[0]
                        conv = convert(dataz[1])
                        savePrivateAcount(conv)
                        private_status = True
                else:
                    private_status = False
            
            if dataPub and dataPub[0] != data_public_old:
                data_public_old = dataPub[0]
                conv = convert(dataPub[1])
                savePublicAcount(conv)
            no += 1
            print(f"PROCESS [ {no} ] REFRESH.. ")
        except Exception as e:
            print("Error : "+str(e))
