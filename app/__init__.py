# to run this website and watch for changes: 
# $ export FLASK_ENV=development; flask run
# site will be available at 
# http://localhost:5000

from flask import Flask, g, render_template, request
import sqlite3

app = Flask(__name__)

# main page
@app.route('/')
def main():
    return render_template('main.html')

# submit page
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try:
            # raise exception for empty fields
            if request.form["handle"] == '' or request.form["message"] == '':
                raise ValueError('Empty fields.')

            # call the database function if successful submission
            insert_message()

            return render_template('submit.html', thanks=True)
        except:
            return render_template('submit.html', error=True)

def get_message_db():
    try:
        return g.message_db
    except:
        # if the database doesn't exist, create one with the given columns
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = \
        '''
        CREATE TABLE IF NOT EXISTS `messages` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            handle TEXT NOT NULL,
            message TEXT NOT NULL
        )
        '''
        cursor = g.message_db.cursor()
        cursor.execute(cmd)

        return g.message_db

def insert_message():
    conn = get_message_db()
    
    # add the handle and message to the database
    cmd = \
    f'''
    INSERT INTO messages (handle, message)
    VALUES ('{request.form["handle"]}', '{request.form["message"]}') 
    '''
    cursor = conn.cursor()
    cursor.execute(cmd)
    conn.commit()
    conn.close()

# view page
@app.route('/view/')
def view():
    return render_template('view.html', messages = random_messages(5))

def random_messages(n):
    conn = get_message_db()

    # get n random rows from the database
    cmd = \
    f'''
    SELECT * FROM messages ORDER BY RANDOM() LIMIT {n}; 
    '''
    cursor = conn.cursor()
    cursor.execute(cmd)

    # store results before closing the connection
    result = cursor.fetchall()
    conn.close()

    return result