from encryption import encrypt
from requests import post,get
from json import loads,dumps
from random import randint
from urllib import request
from pathlib import Path
from os import system
import PIL.Image, base64, io

class colors:
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    RESET = "\033[0m"
    YELLOW = "\033[33m"
    RED = "'\033[31m"
    
class clients:
	android = {"app_name" : "Main","app_version" : "2.9.8","platform" : "Android","package" : "app.rbmain.a","lang_code"   : "fa"}
	
class uploader:
	def __init__(self, auth):
		self.auth = auth
		if len(self.auth) != 32: print("auth must be 32 characters!"); exit()
		self.enc = encrypt(self.auth)

	@staticmethod
	def getURL():
		return "https://messengerg2c64.iranlms.ir/"

	@staticmethod
	def getThumbInline(image_bytes:bytes):
		im = PIL.Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		if height > width:
			new_height = 40
			new_width  = round(new_height * width / height)
		else:
			new_width  = 40
			new_height = round(new_width * height / width)
		im = im.resize((new_width, new_height), PIL.Image.ANTIALIAS)
		changed_image = io.BytesIO()
		im.save(changed_image, format='PNG')
		changed_image = changed_image.getvalue()
		return base64.b64encode(changed_image)

	@staticmethod
	def getImageSize(image_bytes:bytes):
		im = PIL.Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		return [width , height]

	def getChats(self, start_id=None):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({"method":"getChats","input":{"start_id":start_id},"client": clients.android}))},url=uploader.getURL()).json()["data_enc"]))

	def sendchataction(self, chat_id, action):		
		data = {"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({"method":"sendChatActivity","input":{"activity": action,"object_guid": chat_id},"client": clients.android}))}
		return loads(self.enc.decrypt(post(json=data,url=uploader.getURL()).json()["data_enc"]))
	
	def downloader(self, link:str):
	   path = link.split("/")[-1]
	   request.urlretrieve(link, path)
	   
	def requestSendFile(self,file):
	    while True:
	        try:
	            data = {"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({"method":"requestSendFile","input":{"file_name": file.split("/")[-1],"mime": file.split(".")[-1],"size": str(499999)},"client": clients.android}))}
	            return loads(self.enc.decrypt(post(json=data,url=uploader.getURL()).json()["data_enc"]))["data"]
	            break
	        except:pass

	def uploadFile(self,file):
	    frequest = uploader.requestSendFile(self,file)	    
	    bytef , hash_send , file_id , url = open(file,"rb").read() , frequest["access_hash_send"] , frequest["id"] , frequest["upload_url"]
    
	    header = {"auth":self.auth,"Host":url.replace("https://","").replace("/UploadFile.ashx",""),"chunk-size":str(Path(file).stat().st_size),"file-id":str(file_id),"access-hash-send":hash_send,"content-type": "application/octet-stream","content-length": str(Path(file).stat().st_size),"accept-encoding": "gzip","user-agent": "okhttp/3.12.1"}
	        
	    if len(bytef) <= 1000000:
	        
	        header["part-number"], header["total-part"] = "1","1"	        
	        while True:
	            try:
	                j = post(data=bytef,url=url,headers=header).text
	                j = loads(j)['data']['access_hash_rec']
	                break
	            except:continue
	        return [frequest, j]
	    else:	       
	       t = round(((len(bytef) / 1024) / 1024))
	       while True:
	           try:
	               header["chunk-size"], header["part-number"], header["total-part"] = "1", str(1),str(t)
	               o = post(data="1",url=url,headers=header).text
	               o = loads(o)['status']
	               if o == "OK":
	                   break	                   
	               else:	                   
	                   frequest = uploader.requestSendFile(self,file)
	                   bytef , hash_send , file_id , url = open(file,"rb").read() , frequest["access_hash_send"] , frequest["id"] , frequest["upload_url"]
	                   
	                   header = {"auth":self.auth,"Host":url.replace("https://","").replace("/UploadFile.ashx",""),"chunk-size":str(Path(file).stat().st_size),"file-id":str(file_id),"access-hash-send":hash_send,"content-type": "application/octet-stream","content-length": str(Path(file).stat().st_size),"accept-encoding": "gzip","user-agent": "okhttp/3.12.1"}
	           except:continue

	       f = round(len(bytef) / t + 1)
	       for i in range(1,t+1):
	           if i != t:
	               k = i - 1
	               k = k * f
	               while True:
	                   try:
	                       header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:k + f])), str(i),str(t)
	                       o = post(data=bytef[k:k + f],url=url,headers=header).text
	                       s = loads(o)['status']
	                       system("clear")
	                       print(f"{colors.RED}part: {colors.GREEN}{i}{colors.RESET} / {colors.CYAN}{t}{colors.RESET} / {colors.CYAN}status: {colors.RESET}{colors.GREEN}{s}{colors.RESET}")
	                       o = loads(o)['data']
	                       break
	                   except:continue
	           else:
	               k = i - 1
	               k = k * f
	               while True:
	                   try:
	                       header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:k + f])), str(i),str(t)
	                       p = post(data=bytef[k:k + f],url=url,headers=header).text
	                       s_ = loads(p)['status']
	                       system("clear")
	                       print(f"{colors.RED}part: {colors.GREEN}{i}{colors.RESET} / {colors.CYAN}{t}{colors.RESET} / {colors.CYAN}status: {colors.RESET}{colors.GREEN}{s_}{colors.RESET}")
	                       p = loads(p)['data']['access_hash_rec']
	                       break
	                   except:continue
	               return [frequest, p]

	def sendmovie(self,chat_id, file, height, width, duration, caption=None, message_id=None):
	    uresponse = uploader.uploadFile(self,file)
	    thumbnail , file_id , mime , dc_id , access_hash_rec , file_name , size = file , str(uresponse[0]["id"]) , file.split(".")[-1] , uresponse[0]["dc_id"] , uresponse[1] , file.split("/")[-1] , str(len(get(file).content if "http" in file else open(file,"rb").read()))
	    
	    inData = {"file_inline":{"access_hash_rec":access_hash_rec,"auto_play":False,"dc_id":dc_id,"file_id":file_id,"file_name":file_name,"height":height,"mime":mime,"size":size,"thumb_inline":thumbnail,"time":duration,"type":"Video","width":width},"is_mute":False,"object_guid":chat_id,"rnd":f"{randint(100000,999999999)}","reply_to_message_id":message_id}	    
	    
	    if caption != None: inData["text"] = caption

	    data = {"api_version":"4","auth":self.auth,"client":clients.android,"data_enc":self.enc.encrypt(dumps(inData)),"method":"sendMessage"}	    
	    	    
	    while True:
	       try:
	           return loads(self.enc.decrypt(post(json=data,url=uploader.getURL()).json()["data_enc"]))
	           break
	       except: continue

	def sendmusic(self,chat_id, file, artist, duration, caption=None, message_id=None):
	    uresponse = uploader.uploadFile(self,file)	    
	    file_id , mime , dc_id , access_hash_rec , file_name , size = str(uresponse[0]["id"]) , file.split(".")[-1] , uresponse[0]["dc_id"] , uresponse[1] , file.split("/")[-1] , str(len(get(file).content if "http" in file else open(file,"rb").read()))	    
	    
	    inData = {"file_inline":{"access_hash_rec":access_hash_rec,"auto_play":False,"dc_id":dc_id,"file_id":file_id,"file_name":file_name,"height":0.0,"mime":mime,"music_performer":artist,"size":size,"time": duration,"type":"Music","width":0.0},"is_mute":False,"object_guid":chat_id,"rnd":f"{randint(100000,999999999)}","reply_to_message_id":message_id}	    	    
	    
	    if caption != None: inData["text"] = caption 
	    
	    data = {"api_version":"4","auth":self.auth,"client":clients.android,"data_enc":self.enc.encrypt(dumps(inData)),"method":"sendMessage"}	    
	    	    
	    while True:
	       try:
	           return loads(self.enc.decrypt(post(json=data,url=uploader.getURL()).json()["data_enc"]))
	           break
	       except: continue

	def sendfile(self, chat_id, file, caption=None, message_id=None):
	    uresponse = uploader.uploadFile(self,file)	    
	    file_id , mime , dc_id , access_hash_rec , file_name , size = str(uresponse[0]["id"]) , file.split(".")[-1] , uresponse[0]["dc_id"] , uresponse[1] , file.split("/")[-1] , str(len(get(file).content if "http" in file else open(file,"rb").read()))	    
	    
	    inData = {"method":"sendMessage","input":{"object_guid":chat_id,"reply_to_message_id":message_id,"rnd":f"{randint(100000,999999999)}","file_inline":{"dc_id":str(dc_id),"file_id":str(file_id),"type":"File","file_name":file_name,"size":size,"mime":mime,"access_hash_rec":access_hash_rec}},"client": clients.android}	    
	    
	    if caption != None: inData["input"]["text"] = caption
	    
	    data = {"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps(inData))}
   
	    while True:
	        try:
	            return loads(self.enc.decrypt(loads(post(json=data,url=uploader.getURL()).text)['data_enc']))
	            break
	        except: continue

	def sendvoice(self, chat_id, file, duration, caption=None, message_id=None):
		uresponse = uploader.uploadFile(self, file)		
		file_id , mime , dc_id , access_hash_rec , file_name , size = str(uresponse[0]["id"]) , file.split(".")[-1] , uresponse[0]["dc_id"] , uresponse[1] , file.split("/")[-1] , str(len(get(file).content if "http" in file else open(file,"rb").read()))

		inData = {"method":"sendMessage","input":{"file_inline": {"dc_id": dc_id,"file_id": file_id,"type":"Voice","file_name": file_name,"size": size,"time": duration,"mime": mime,"access_hash_rec": access_hash_rec,},"object_guid":chat_id,"rnd":f"{randint(100000,999999999)}","reply_to_message_id":message_id},"client": clients.android}
		
		if caption != None: inData["input"]["text"] = caption
	    
		data = {"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps(inData))}

		while True:
			try:
				return loads(self.enc.decrypt(loads(post(json=data,url=uploader.getURL()).text)['data_enc']))
				break
			except: continue

	def sendimage(self, chat_id, file, thumbnail=None, caption=None, message_id=None):	
		uresponse = uploader.uploadFile(self, file)
		file_id , mime , dc_id , access_hash_rec , file_name , Size , size = str(uresponse[0]["id"]) , file.split(".")[-1] , uresponse[0]["dc_id"] , uresponse[1] , file.split("/")[-1] , str(len(get(file).content if "http" in file else open(file,"rb").read())) , []
				
		if thumbnail == None: thumbnail = file
		elif "." in thumbnail:thumbnail = str(uploader.getThumbInline(open(file,"rb").read() if not "http" in file else get(file).content))

		if size == []: size = uploader.getImageSize(open(file,"rb").read() if not "http" in file else get(file).content)

		file_inline = {"dc_id": dc_id,"file_id": file_id,"type":"Image","file_name": file_name,"size": Size,"mime": mime,"access_hash_rec": access_hash_rec,"width": size[0],"height": size[1],"thumb_inline": thumbnail}			
		inData = {"method":"sendMessage","input":{"file_inline": file_inline,"object_guid": chat_id,"rnd": f"{randint(100000,999999999)}","reply_to_message_id": message_id},"client": clients.android}
		
		if caption != None: inData["input"]["text"] = caption
		
		data = {"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps(inData))}
						
		while True:
		    try:
		        return loads(self.enc.decrypt(post(json=data,url=uploader.getURL()).json()["data_enc"]))
		        break
		    except: continue

	def sendgif(self, chat_id, file, height, width, caption=None, message_id=None):
	    uresponse = uploader.uploadFile(self,file)
	    file_id , mime , dc_id , access_hash_rec , file_name , size = str(uresponse[0]["id"]) , file.split(".")[-1] , uresponse[0]["dc_id"] , uresponse[1] , file.split("/")[-1] , str(len(get(file).content if "http" in file else open(file,"rb").read()))
	    
	    file_inline ={"access_hash_rec":access_hash_rec,"auto_play":False,"dc_id":dc_id,"file_id":file_id,"file_name":file_name,"height":height,"mime":mime,"size":size,"thumb_inline":file,"time":60,"type":"Gif","width":width}
	    inData = {"method":"sendMessage","input":{"file_inline":file_inline,"is_mute":False,"object_guid":chat_id,"rnd":f"{randint(100000,999999999)}","reply_to_message_id": message_id},"client":clients.android}
	    
	    if caption != None: inData["input"]["text"] = caption
	    
	    data = {"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps(inData))}

	    if caption != None: inData["input"]["text"] = caption
	    
	    while True:
	       try:
	           return loads(self.enc.decrypt(post(json=data,url=uploader.getURL()).json()["data_enc"]))
	           break
	       except: continue