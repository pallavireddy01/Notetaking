from pymongo import MongoClient
from flask import Flask,request,jsonify

client=MongoClient('127.0.0.1',27017)
db=client['app']
collection=db['registration']
collection1=db['notetaking']
 
backend = Flask(__name__)

@backend.route('/')
def homepage():
    return 'API server started.'

@backend.route('/signup',methods=['get'])
def signup():
    username = request.args.get("username")
    password = request.args.get("password")
    k={}
    k['_id']=username
    k['username']=username
    k['password']=password
    print(k)
    try:
        collection.insert_one(k)
        return 'sign up success'
    except:
        return 'signup failure'

@backend.route('/login',methods=['get'])
def login():
    username=request.args.get('username')
    password=request.args.get('password')
    flag=0
    for i in collection.find({'_id':username}):
        if(password==i['password']):
            flag=1
            return 'loggedin successfully'
        if(flag==0):
            return 'check password and username once!!'
    
@backend.route('/givenote',methods=['get'])
def givenote():
    owner=request.args.get('owner')
    title = request.args.get('title')
    note = request.args.get('note')
    collection1=db['notetaking']
    k={}
    k['id']=title
    k['title']=title
    k['note']=note
    k['owner']=owner
    collection1.insert_one(k)
    return 'note taken'


@backend.route('/viewnote',methods=['get'])
def viewnotes():
    owner=request.args.get('owner')
    # title=request.args.get('title')
    data=[]
    for i in collection1.find({'owner':owner}):
        d=[]
        d.append(i['title'])
        d.append(i['note'])
        data.append(d)
    return jsonify({'data':data})


if(__name__ == '__main__'):
    backend.run(host='0.0.0.0',port=4000,debug=True)