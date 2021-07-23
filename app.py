import sqlite3
from flask import *


def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS students (name TEXT, addr TEXT, city TEXT, code TEXT)")
    print('Table created successfully')
    conn.close()


init_sqlite_db()

app = Flask(__name__)


@app.route('/enter-new/')
def enter_new_student():
    template_name = 'student.html'
    return render_template(template_name)


@app.route('/add-new-record/', methods=["POST"])
def add_new_record():
    msg = None
    if request.method == "POST":
        try:
            name = request.form['name']
            address = request.form['addr']
            city = request.form['city']
            code = request.form['code']

            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO students (name,addr,city,code) VALUES (?,?,?,?)", (name, address, city, code))
                conn.commit()
                msg = "Record added successfully."

        except Exception as e:
            conn.rollback()
            msg = "Error occurred during the insert operation: " + str(e)
        finally:
            conn.close()
            return render_template('results.html', msg=msg)


if __name__ == '__main__':
    app.debug = True
    app.run()
