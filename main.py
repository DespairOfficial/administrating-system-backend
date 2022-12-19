import shutil
from typing import Union
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil

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

@app.get("/domens")
def getDomens():
	list_of_apache_domens = os.listdir("./apache")
	list_of_nginx_domens = os.listdir("./nginx")
	list_of_domens = []
	for apache_domen in list_of_apache_domens:
		list_of_domens.append({
			"name": apache_domen,
			"server": "apache"
		})
	for nginx_domen in list_of_nginx_domens:
		list_of_domens.append({
			"name": nginx_domen,
			"server": "nginx"
		})
	return {"domens": list_of_domens}


class DomenModel(BaseModel):
	name: str
	server: str


@app.post("/domens")
def getDomens(domen_model: DomenModel):
	cwd = os.getcwd()
	target_dir = cwd +'/' + domen_model.server + '/' + domen_model.name
	os.mkdir(target_dir)
	with open(target_dir +'/index.html', 'w') as fp:
		fp.write(domen_model.name + ' by ' + domen_model.server)

@app.post("/domens/delete")
def getDomens(domen_model: DomenModel):
	cwd = os.getcwd()
	target_dir = cwd +'/' + domen_model.server + '/' + domen_model.name
	shutil.rmtree(target_dir)



if __name__ == "__main__":
	uvicorn.run('main:app', port= 8000, host="127.0.0.1", reload=True)