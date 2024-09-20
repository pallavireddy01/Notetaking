from flask import Flask,render_template,request,json,redirect,session
import urllib3

frontend=Flask(__name__)
frontend.secret_key="143151"

backend='http://127.0.0.1:4000'

signupapi=backend+'/signup'
loginapi=backend+'/login'
givenoteapi=backend+'/givenote'
viewnoteapi=backend+'/viewnote'

@frontend.route('/')
def homepage():
    return render_template('index1.html')

@frontend.route('/givenote')
def givenote():
    return render_template('givenote.html')



@frontend.route('/signupform',methods=['post'])
def signupform():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    http=urllib3.PoolManager()
    response=http.request('get',signupapi+'?username='+username+'&password='+password)
    response=response.data
    response=response.decode('utf-8')
    if response=="sign up failure":
        return render_template('index1.html',err='sign up failure')
    else:
        return render_template('index1.html',res="successful")


@frontend.route('/loginform',methods=['post'])
def loginform():
    username=request.form['username1']
    password=request.form['password1']
    http=urllib3.PoolManager()
    response=http.request('get',loginapi+'?username='+username+'&password='+password)
    response=response.data
    response=response.decode('utf-8')
    if response=='you are not authorized':
        return render_template('index1.html',err='you are not authorized')
    else:
        session['username']=username
        return redirect('/givenote')

@frontend.route('/logout')
def logout():
    session['/username']=None
    return redirect('/')

@frontend.route('/givenoteform',methods=['post'])
def gt():
    owner=session['username']
    title=request.form['title']
    note=request.form['note']
    http=urllib3.PoolManager()
    response=http.request('get',givenoteapi+'?title='+title+'&note='+note+'&owner='+owner)
    response=response.data
    response=response.decode('utf-8')
    return render_template('givenote.html',res='note taken')


@frontend.route('/viewnote')
def vn():
    owner=session['username']
    http=urllib3.PoolManager()
    response=http.request('get',viewnoteapi+'?owner='+owner)
    response=response.data
    response=response.decode('utf-8')
    response=json.loads(response)
    response=response['data']
    l=len(response)
    return render_template('viewnote.html',data=response,l=l)

if __name__=="__main__":
    frontend.run(host='0.0.0.0',port=7000,debug=True)