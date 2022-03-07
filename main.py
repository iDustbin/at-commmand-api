from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.openapi.utils import get_openapi
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
import random
import uvicorn
from pydantic import BaseModel
import serial
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import re
from serial import *

# ports = serial.tools.list_ports.comports()

# for port, desc, hwid in sorted(ports):
#         print("{}: {} [{}]".format(port, desc, hwid))

app = FastAPI()
# optional, required if you are serving static files
#app_app.mount("/static", StaticFiles(directory="static"), name="static")
# optional, required if you are serving webpage via template engine
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost",
    "http://localhost:8003",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# depends on use cases
class Item(BaseModel):
    language = 'english'

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="DNSMasq API",
        version="1.1.0",
        description="DNSMasq API",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# @app.get("/", response_class=PlainTextResponse)
# async def hello():
#     return "Hello World!"

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@app.get("/ATI/", tags=["Device Information"])
def display_identification_information():
    serialconsole = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=1)
    serialconsole.write(bytes("ATI\r\n", 'utf-8'))
    #msg = serialconsole.read(32798)
    msg = serialconsole.readline().decode("utf-8")
    #print(msg)
    serialconsole.close() 
    return serialconsole


@app.get("/AT/GMI/", tags=["Device Information"])
async def manufacturer_identification():
    gmi = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=1)
    gmi.write(bytes("AT+GMI\r\n", 'utf-8'))
    #gmi.read(32798)
    data = gmi.readline().decode("utf-8")
    gmi.close() 
    return data


@app.get("/AT/GMM/", tags=["Device Information"])
async def request_model_identification():
    serialconsole = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=1)
    serialconsole.write(bytes("AT+GMM\r\n", 'utf-8'))
    
    #data = serialconsole.read(32798)
    
    #msg = gmm.readline().decode("utf-8")
    
    data = serialconsole.readline().decode("utf-8")
    
    return data
    serialconsole.close() 

@app.get("/AT/GMM/", tags=["Firmware Information"])
async def request_firmware_revision_identification():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(bytes("AT+GMR\r\n", 'utf-8'))
    return console
    console.close() 

@app.get("/AT/GSN/", tags=["IMEI"])
async def request_international_mobile_equipment_identity():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(b'AT+GSN')
    return console
    console.close() 

@app.get("/AT/CGSN/", tags=["IMEI"])
async def request_international_mobile_equipment_identity():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(b'AT+CGSN')
    return console
    console.close() 

@app.get("/AT/CIMI/", tags=["IMSI"])
async def request_international_mobile_subscriber_identity():
    cimi = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    cimi.write(bytes("AT+CIMI\r\n", 'utf-8'))
    cimi.read(32798)
    cimi.readline().decode("utf-8")
    return cimi
    cimi.close() 

@app.get("/AT/CREG/", tags=["Network Registration Status"])
async def network_registration_status():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(b'AT+CREG')
    return console
    console.close() 

@app.get("/AT/CSQ/", tags=["Signal Quality"])
async def signal_quality_report():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(b'AT+CSQ')
    return console
    console.close() 

@app.get("/AT/CTZU/?", tags=["TimeZone"])
async def automatic_time_zone_update():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(b'AT+CTZU=?')
    return console
    console.close() 

@app.get("/AT/CTZU/ON", tags=["TimeZone"])
async def automatic_time_zone_update_on():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(b'AT+CTZU=on')
    # enable_disable = {'text': text}
    return console
    console.close()

@app.get("/AT/QRSRP", tags=["RSRP"])
async def report_RSRP():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(b'AT+QRSRP')
    return console
    console.close()

@app.get("/AT/QSINR", tags=["SINR"])
async def Report_SINR():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(b'AT+QSINR')
    return console
    console.close()

@app.get("/AT/QNWINFO", tags=["Network Information"])
async def query_network_information():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(b'AT+QNWINFO')
    return console
    console.close()

@app.get("/AT/QSPN", tags=["Provider Name"])
async def query_the_service_provider_name():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(b'AT+QNWINFO')
    return console
    console.close()

@app.get("/AT/QENG/ServingCell", tags=["Serving Cell"])
async def query_servingcell():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(b'AT+QENG="servingcell"')
    return console
    console.close()

@app.get("/AT/QENG/NeighbourCell", tags=["Neighbour Cell"])
async def query_neighbourCell():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(b'AT+QENG="neighbourcell"')
    return console
    console.close()

@app.get("/AT/QNWCFG", tags=["Network Speed"])
async def get_average_uplink_rate_and_downlink_rate():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(b'AT+QNWCFG="up/down"')
    return console
    console.close()

@app.get("/AT/QNWPREFCFG", tags=["Network Speed"])
async def get_average_uplink_rate_and_downlink_rate():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(b'AT+QNWPREFCFG="nsa_nr5g_band"')
    return jsonable_encoder ({ console }), 200
    console.close()

@app.get("/AT/QGDNRCNT", tags=["Sent & Received"])
async def Query_the_current_bytes_sent_and_received():
    console = serial.Serial("/dev/cu.usbserial-14131130",  115200, timeout=5)
    console.write(b'AT+QGDNRCNT?')
    return jsonable_encoder ({ console }), 200
    console.close()


@app.get('/api/dnsmasq/version')
async def version():
    os.system("dnsmasq -v")
    return jsonable_encoder({'version'}), 200

@app.get('/api/dnsmasq/status')
async def status():
    os.system("dnsmasq status")
    return jsonable_encoder({'status'}), 200

# {
#     "name": "Foo",
#     "description": "An optional description",
#     "price": 45.2,
#     "tax": 3.5
# }

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

# @app.post("/items/")
# async def create_item(item: Item):
#     return item

@app.get('/alpha')
async def alpha(text: str):
    result = {'text': text, 'is_alpha' : text.isalpha()}
    return result

# was ist das hier ? 
#class add_host(BaseModel):
    # mac_address = {'mac': text.replace(":", "-")}
    # ip_address = {'ip_address': text}
    # host_name = {'host_name': text}
    # lease_time = {'lease_time': text}
    #description: str = Test
    # price: float
    # tax: Optional[float] = None

@app.post('/add/host')
async def add_2_host(text: str):
    mac_address = {'mac': text.replace(":", "-")}
    ip_address = {'ip_address': text}
    host_name = {'host_name': text}
    lease_time = {'lease_time': text}

    return mac_address, ip_address, host_name, lease_time

@app.post('/api/dnsmasq/add/host')
async def add_host():
    new_host = request.get_json()['mac']
    ip_address = request.get_json()['ip']
    host_name = request.get_json()['hostname']
    lease_time = request.get_json()['lease']
    os.system("echo "+"dhcp-host="+str(new_host+',')+str(ip_address+',')+str(host_name+',')+str(lease_time)+" >> /etc/dnsmasq.conf")    
    mac_address_replace = request.get_json()['mac'].replace(":", "-")
    parent_dir = "/var/lib/tftpboot/pxelinux.cfg/"
    add_host = os.path.join('/var/lib/tftpboot/pxelinux.cfg/' + request.get_json()['mac'].replace(":", "-"))
    add_host = os.path.join(parent_dir, add_host) 
    os.makedirs(add_host) 
    print(add_host)
    if not os.path.isdir('/var/lib/tftpboot/pxelinux.cfg'):
         os.mkdir('/var/lib/tftpboot/pxelinux.cfg/'+ new_host)
    os.mkdir(new_host)
    return jsonable_encoder({}), 200

@app.get('/api/dnsmasq/hosts')
async def hosts():
    dhcp_hosts = []
    f = open("/etc/dnsmasq.conf")
    dns_conf = f.read()
    f.close()
    confs = dns_conf.split('\n')
    for i in range(len(confs)):
        print(i)
        if confs[i].split('=')[0] == 'dhcp-host':
            host = confs[i].split('=')[1]
            dhcp_hosts.append(host)
            # dhcp_hosts.append(host.split(','))
    # return {'dhcp_host': dhcp_hosts}, 200
    return jsonable_encoder({'dhcp_host': dhcp_hosts}), 200

@app.post('/api/dnsmasq/config/load')
async def config():
    os.system("dnsmasq --conf-file=/etc/dnsmsq.conf")
    return jsonable_encoder({'status'}), 200

@app.route('/api/dnsmasq/config/resolv')
async def resolv():
    os.system("dnsmsq --no-resolv")
    return jsonify({'status'}), 200

@app.route('/ping', methods=['GET'])
async def ping_pong():
    return jsonify('pong!')

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000)