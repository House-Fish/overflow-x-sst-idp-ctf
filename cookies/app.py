from flask import Flask, redirect, url_for, request, render_template, make_response
import base64

app = Flask(__name__)


@app.route('/')
def index():
    if 'session' in request.cookies:
        return redirect(url_for('home', username=base64.b64decode(request.cookies.get('session')).decode('utf-8')))
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        token = { "username" : username }
        
        if username == 'user' and password == 'test123':
            session = base64.b64encode(str(token).encode('utf-8'))
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('session', session.decode('utf-8'))
            return resp
        
    return render_template('login.html')

@app.route('/home')
def home():
    if 'session' in request.cookies:
        return render_template('home.html', username=base64.b64decode(request.cookies.get('session')).decode('utf-8')[14:-2])
    return f"You are not logged in <br><a href = {url_for('index')}>click here to login</a>"

@app.route('/admin')
def admin():
    token = base64.b64decode(request.cookies.get('session')).decode('utf-8')
    
    if ('session' in request.cookies) and ('admin' in token):
        return render_template('admin.html')
    return f"Not an admin. <br> <a href = {url_for('home')}>Go back</a>"


@app.route('/logout')
def logout():
    resp = redirect(url_for('index'))
    resp.delete_cookie('session')
    return resp

if __name__ == "__main__":
    app.run()