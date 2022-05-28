# to run this website and watch for changes: 
# $ export FLASK_ENV=development; flask run


from flask import Flask, g, render_template, request
import numpy as np
import sqlite3


# Create web app, run with flask run
# (set "FLASK_ENV" variable to "development" first!!!)

app = Flask(__name__)

# Create main page

@app.route('/')

# after running
# $ export FLASK_ENV=development; flask run
# site will be available at 
# http://localhost:5000

def main():
    return render_template('main.html')

#submit page
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        #try:
        # raise exception for empty fields
        if request.form["name"] == '' or request.form["message"] == '':
            raise ValueError('Empty fields.')

        # call the database function if successful submission
        insert_message(request)

        return render_template('submit.html', thanks=True)
        #except:
            #return render_template('submit.html', error=True)

def get_message_db():
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = \
        '''
        CREATE TABLE IF NOT EXISTS `messages` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            handle TEXT NOT NULL,
            message TEXT NOT NULL
        );
        '''
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
        return g.message_db

def insert_message(request):
    conn = get_message_db()
    cmd = \
    f'''
    INSERT INTO messages (handle, message)
    VALUES ('{request.form["name"]}', '{request.form["message"]}') 
    '''
    cursor = conn.cursor()
    cursor.execute(cmd)
    conn.commit()
    conn.close()


@app.route('/view/')
def view():
    return render_template('view.html', messages = random_messages(5))

def random_messages(n):
    # refer to insert_messages and discussion view function 
    # HINT SQL command - ORDER BY RANDOM()
    conn = get_message_db()
    cmd = \
    f'''
    SELECT * FROM messages ORDER BY RANDOM() LIMIT 5; 
    '''
    cursor = conn.cursor()
    cursor.execute(cmd)
    result = cursor.fetchall()
    conn.close()
    return result