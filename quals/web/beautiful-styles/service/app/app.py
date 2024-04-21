from flask import Flask, render_template, request, redirect, flash, send_from_directory
from os import environ, urandom
from uuid import uuid4
import socket

app = Flask(__name__)
app.config["SECRET_KEY"] = environ.get('SECRET_KEY', urandom(128).hex())
app.config['UPLOAD_FOLDER'] = './uploads'
ADMIN_HOST = environ.get('ADMIN_HOST', 'web-css-leak-admin')
ADMIN_PORT = int(environ.get('ADMIN_PORT', 3001))

with open('./templates/site.html', 'r') as f:
    SITE_TEMPLATE = f.read()


@app.route('/')
def index():
    return render_template('index.html', site_template=SITE_TEMPLATE)

@app.route('/submit', methods=['POST'])
def submit():
    css_value = request.form.get("css_value")
    if css_value is None or len(css_value) == 0:
        flash('No CSS value provided', 'danger')
        return redirect('/')

    submit_id = str(uuid4())
    with open(f'./uploads/{submit_id}.css', 'w') as f:
        f.write(css_value)
    return redirect(f'/submission/{submit_id}')


@app.route('/submission/<string:submit_id>')
def submission(submit_id):
    flag = request.cookies.get('admin_flag', 'grey{this_is_a_fake_flag}')
    return render_template('site.html', submit_id=submit_id, flag=flag)

@app.post('/judge/<string:submit_id>')
def judge(submit_id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ADMIN_HOST, ADMIN_PORT))
    s.sendall(submit_id.encode())
    s.close()
    return render_template('judged.html')

@app.route('/uploads/<path:filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
