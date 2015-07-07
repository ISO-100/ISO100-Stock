from flask import render_template
from flask import Flask

app=Flask(__name__)
@app.route('/')
@app.route('/index')
def index():
    user ={ 'nickname': 'Miguel'} # fake user
    return render_template("index.html",
    title ='Home',
    user =user)

if __name__ == '__main__':
    app.debug = True
    app.run()