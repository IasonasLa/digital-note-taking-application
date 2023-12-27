import pymongo
from pymongo import MongoClient
from flask import Flask, request,Response,redirect,jsonify
import json
from datetime import date
import os

mongodb_hostname = os.environ.get("MONGO_HOSTNAME","Localhost")
client = MongoClient('mongodb://'+mongodb_hostname+':27017')


db = client['DigitalNotes']

users = db['users']
admins = db['admins']
userNotes = db['user notes']







app =  Flask(__name__)
global flageiros
flageiros = 0

@app.route('/new',methods=['POST','GET'])
def new():
	if request.method=='POST':
		data = None
		data = json.loads(request.data)
		email=data['email']
		username=data['username']
		fullname=data['fullname']
		password=data['password']
		if users.count_documents({"email":email}) == 0 :
			newUser= {"email":email,"username":username,"fullname":fullname,"password":password}
			users.insert_one(newUser)
			
			return Response("new User added",status=200,mimetype='application/json')
		else:
			return Response("A user with the given email already exists",status=200,mimetype='application/json')
	
			
@app.route('/login',methods=['POST','GET'])
def login():
	if request.method=='POST':
		data = None
		data = json.loads(request.data)
		userinfo = data['userinfo']
		password = data['password']
		if users.find({"username":userinfo}) is not None :
			if users.count_documents({"username":userinfo}) !=0 :
				usernamexx=users.find_one({"username":userinfo})
				if (usernamexx['password'] == password):
					global flageiros 
					flageiros = 1
					print(password)
					print(list(usernamexx))
					return 'You have connected succesfully'
				else :
					return 'wronge password'
			else:
				return 'the users doesnot exist'		

@app.route ('/newNote',methods=['POST','GET'])
def newNote():
	if request.method=='POST':
		if (flageiros==1):
			data = None
			data = json.loads(request.data)
			title = data['title']
			note = data['note']
			key = data['key']
			today = date.today()
			d=today.strftime("%d/%m/%Y")
			new={"title":title,"note":note,"key":key,"date":d}
			print(new)
			userNotes.insert_one(new)
			return 'your new note has been created'
			
			
		
		
		
		else:
			return 'you need to login first!'
	

@app.route('/searchNote',methods=['POST','GET'])
def search():
	if ((request.method=='POST') and (flageiros==1)):
		data=None
		data=json.loads(request.data)
		title=data['title']
		if userNotes.count_documents({"title":title}) != 0:
			find=userNotes.find_one({"title":title})
			printtitle=find['title']
			printnote=find['note']
			printkey=find['key']
			str="title: "+ printtitle +" Note :"+ printnote +" Key: "+ printkey
			return str
		else :
			return 'there is not any note with that title'
	else :
		return 'you need to login first!'
				
				
				
				
@app.route('/searchByKey',methods=['POST','GET'])
def serchkey():
	if request.method=='POST' and flageiros==1 :
		data=None
		data=json.loads(request.data)
		key=data['key']
		if userNotes.count_documents({"key":key})!=0:
			find=userNotes.find_one({"key":key})
			printtitle=find['title']
			printnote=find['note']
			printkey=find['key']
			str="title: "+ printtitle +" Note :"+ printnote +" Key: "+ printkey
			return str
			
		else:
			return 'there is no such a key'
	else:
		return 'you need to login first'
		
@app.route('/update',methods=['POST','GET'])
def updateTitle():
	if request.method=='POST' and flageiros==1 :
		data=None
		title=data['title']
		newtitle=data['newtitle']
		if userNotes.count_documents({"title":title}) !=0 :
			if newtitle!=None:
				userNotes.updateOne({"title":title},{"$set":{'title':newtitle}}) 
				find=userNotes.find_one({"title":newtitle})
				print(find['title'])
				return 'you have change the title of the note !'
			else:
				return 'Bad user input...'
			
			
		
		else:
			return 'this title does npt exist'	
	else:
		return 'you need to login first'	
	
@app.route('/deleteNote',methods=['POST','GET'])
def delnote():
	if request.method=='POST' and flageiros==1 :
		data=None
		data=json.loads(request.data)
		title=data['title']
		if userNotes.count_documents({"title":title}) !=0:
			userNotes.delete_one({"title":title})
			return 'the note has been deleted'
		else:
			return 'this title does not exist'
	
	else:
		return 'you need to login first'			

@app.route('/delAcc',methods=['POST','GET'])
def delacc():
	if request.method=='POST' and flageiros==1 :
		data=None
		data=json.loads(request.data)
		username=data['username']
		password=data['password']
		if users.count_documents({"username":username})!=0:
			find=users.find_one({"username":username})
			passwordxx=find['password']
			if passwordxx==password:
				users.delete_one({"username":username})
				return 'youre account has been deleted'
				
			else:
				return 'wrong password'	
		else:
			return 'there is not an account with than name'
	else:
		return 'you need to login first'



@app.route ('/admin',methods=['POST','GET'])
def adminenter():
	if request.method=='POST':
		data = None
		#try:
		data = json.loads(request.data)
		#except Exception as e:
			#return Response("bad json content",status=500,mimetype='application/json')
		#if data !=None:
		print(data)
		admin=data['admin']
		password=data['password']
		admin = {"user": admin,"password":password}
		admins.insert_one(admin)
	print(admin,password)
	
	return 'ok'
	
	 	
	
	
	




if __name__=='__main__':
	app.run(debug=True,port=5000)
