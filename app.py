from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'car.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            model TEXT NOT NULL,
            brand TEXT NOT NULL,
            color TEXT,
            price INTEGER
        );
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    cars = conn.execute('SELECT * FROM cars').fetchall()
    conn.close()
    return render_template('index.html', cars=cars)

@app.route('/car', methods=['POST'])
def add_car():
    name = request.form['name']
    model = request.form['model']
    brand = request.form['brand']
    color = request.form['color']
    price = request.form['price']

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO cars (name, model, brand, color, price)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, model, brand, color, price))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:car_id>')
def delete_car(car_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM cars WHERE id = ?', (car_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update/<int:car_id>', methods=['POST'])
def update_car(car_id):
    name = request.form['name']
    model = request.form['model']
    brand = request.form['brand']
    color = request.form['color']
    price = request.form['price']

    conn = get_db_connection()
    conn.execute('''
        UPDATE cars
        SET name = ?, model = ?, brand = ?, color = ?, price = ?
        WHERE id = ?
    ''', (name, model, brand, color, price, car_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
