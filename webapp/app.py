from flask import Flask, render_template, url_for, redirect, session, request

app = Flask(__name__)
app.secret_key = 'team3'

@app.route('/')
def index():
    if 'username' not in session:
        return render_template('login.html')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # from remember me
        if 'username' in session:
            return redirect(url_for('index'))
        
        # If not log in
        return render_template('login.html')
    else: 
        # get data
        username = request.form['username']
        remember_me = request.form['remember_me']
        session['username'] = username
        # if remember me is true, set the session lifetime
        if remember_me:
            from datetime import timedelta
            app.permanent_session_lifetime = timedelta(days= 150)
        # goto index page
        return redirect(url_for('index'))
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    ...

@app.route('/logout')
def logout():
    ...

if __name__ == '__main__':
    app.run(debug=True)