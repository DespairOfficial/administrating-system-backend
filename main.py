import shutil
from typing import Union
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
	"http://localhost:3000",
	"*"
]
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/proxy/isOn")
def checkIsProxyOn():

	result = os.popen("sed -n '1p' /etc/squid/squid.conf").read() 
	if(result.strip()=='# http_acccess deny all'):
		return {"status": 1, "message":"Proxy is off!"}
	elif(result.strip()=='http_access deny all'):
		return {"status": 2, "message":"Proxy is on!"}
	else:
		return {"status": 0, "message":"Error"}

	

@app.get("/proxy/on")
def onProxy():
	os.popen("sed -i '1s/# http_access deny all/http_access deny all/' /etc/squid/squid.conf").read()
	os.popen("systemctl restart squid").read()

	return {"status": 2, "message":"Proxy is on!"}

@app.get("/proxy/off")
def offProxy():
	os.popen("sed -i '1s/http_access deny all/# http_access deny all/' /etc/squid/squid.conf").read()
	os.popen("systemctl restart squid").read()
	return {"status": 1, "message":"Proxy is off!"}


if __name__ == "__main__":
	uvicorn.run('main:app', port= 8000, host="127.0.0.1", reload=True)