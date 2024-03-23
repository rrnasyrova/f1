from flask import Flask, send_file, render_template, request, jsonify, redirect, url_for
import mysql.connector
from datetime import datetime
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
from ml.prediction import *

app = Flask(__name__, static_folder='public')

@app.route('/')
def index():
    return app.send_static_file('html/index.html')

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '22Romashka',
    'database': 'formula1'
}

@app.route('/api/drivers')
def get_drivers():

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM drivers")
    result = cursor.fetchall()

    drivers_list = [{'name': driver[1], 'photo': driver[2], 'id': driver[0]} for driver in result]

    return jsonify(drivers_list)

@app.route('/api/drivers/<int:driver_id>')
def get_driver(driver_id):

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM drivers WHERE id=" + str(driver_id))
    result = cursor.fetchone()

    date_obj = result[4]
    date_str = str(date_obj)

    birthdate = datetime.strptime(date_str, "%Y-%m-%d")

    formatted_date = birthdate.strftime("%d %B %Y")

    months = {
    'January': 'января',
    'February': 'февраля',
    'March': 'марта',
    'April': 'апреля',
    'May': 'мая',
    'June': 'июня',
    'July': 'июля',
    'August': 'августа',
    'September': 'сентября',
    'October': 'октября',
    'November': 'ноября',
    'December': 'декабря'
    }

    month_en = date_obj.strftime("%B")
    month_ru = months[month_en]

    formatted_date_ru = formatted_date.replace(month_en, month_ru) 

    driver_info = {
        'name': result[1],
        'photo2': result[3],
        'birth_date': formatted_date_ru,
        'country': result[5],
        'sideNumber': result[6],
        'team': result[7],
        'titlesWC': result[8]
    }

    cursor.close()
    connection.close()
    
    return jsonify(driver_info)

@app.route('/api/tracks')
def get_tracks():

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT id, name_ru, name_eng, img1 FROM tracks")
    result = cursor.fetchall()

    tracks_list = [{'id': track[0], 'name_ru': track[1], 'name_eng': track[2], 'img1': track[3]} for track in result]

    return jsonify(tracks_list)

@app.route('/api/tracks/<int:track_id>')
def get_track(track_id):

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tracks WHERE id=" + str(track_id))
    result = cursor.fetchone()

    track_info = {
        'heading': result[3],
        'img2': result[5],
        'lenght': result[6],
        'circles': result[7],
        'firstGP': result[8],
        'fastest_lap': result[9]
    }

    cursor.close()
    connection.close()

    
    return jsonify(track_info)

@app.route('/api/add_driver', methods=['POST'])
def add_driver():

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    name = request.form.get('name')
    image1 = request.form.get('image1')
    image2 = request.form.get('image2')
    birth_date = request.form.get('birth_date')
    country = request.form.get('country')
    sideNumber = request.form.get('sideNumber')
    team = request.form.get('team')
    titlesWC = request.form.get('titlesWC')

    sql = "INSERT INTO drivers (name, image1, image2, birth_date, country, sideNumber, team, titlesWC) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (name, image1, image2, birth_date, country, sideNumber, team, titlesWC)

    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()

    return 'Водитель успешно добавлен'

@app.route('/api/add_track', methods=['POST'])
def add_track():

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    name_ru = request.form.get('name_ru')
    name_eng = request.form.get('name_eng')
    heading = request.form.get('heading')
    img1 = request.form.get('image1')
    img2 = request.form.get('image2')
    lenght = request.form.get('lenght')
    circles = request.form.get('circles')
    firstGP = request.form.get('firstGP')
    fastest_lap = request.form.get('fastest_lap')

    sql = "INSERT INTO tracks (name_ru, name_eng, heading, img1, img2, lenght, circles, firstGP, fastest_lap) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (name_ru, name_eng, heading, img1, img2, lenght, circles, firstGP, fastest_lap)

    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()

    return 'Трасса успешно добавлена'

@app.route("/api/delete_driver/<driver_name>", methods=["DELETE"])
def delete_driver(driver_name):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM drivers WHERE name ='" + driver_name + "'")
        connection.commit()

        return jsonify({"message": f"Гонщик {driver_name} успешно удален"})

    except Exception as e:
        return jsonify({"message": f"Ошибка при удалении гонщика: {str(e)}"}), 500

@app.route("/api/delete_track/<track_name>", methods=["DELETE"])
def delete_track(track_name):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM tracks WHERE name_eng ='" + track_name + "'")
        connection.commit()

        return jsonify({"message": f"Трасса {track_name} успешно удалена"})

    except Exception as e:
        return jsonify({"message": f"Ошибка при удалении трассы: {str(e)}"}), 500
    
@app.route('/api/update_driver', methods=['PATCH'])
def update_data_driver():
    data = request.json
    name = data['name']
    sideNumber = data['sideNumber']
    team = data['team']
    titlesWC = data['titlesWC']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    sql = "UPDATE drivers SET sideNumber =%s, team = %s, titlesWC = %s WHERE name = %s"
    val = (sideNumber, team, titlesWC, name)
    cursor.execute(sql, val)

    connection.commit()

    return jsonify(message='Данные успешно обновлены')

@app.route('/api/update_track', methods=['PATCH'])
def update_data_track():
    data = request.json
    name_eng = data['name_eng']
    lenght = data['lenght']
    circles = data['circles']
    fastest_lap = data['fastest_lap']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    sql = "UPDATE tracks SET lenght =%s, circles = %s, fastest_lap = %s WHERE name_eng = %s"
    val = (lenght, circles, fastest_lap, name_eng)
    cursor.execute(sql, val)

    connection.commit()

    return jsonify(message='Данные успешно обновлены')

@app.route('/plot_1')
def plot_1():
    return send_file('data_plot/plot_1.png', mimetype='image/png')

@app.route('/plot_2')
def plot_2():
    return send_file('data_plot/plot_2.png', mimetype='image/png')

@app.route('/plot_3')
def plot_3():
    return send_file('data_plot/plot_3.png', mimetype='image/png')

@app.route('/plot_4')
def plot_4():
    return send_file('data_plot/plot_4.png', mimetype='image/png')

@app.route('/plot_5')
def plot_5():
    return send_file('data_plot/plot_5.png', mimetype='image/png')

@app.route('/api/result_prediction', methods=['GET', 'POST'])
def show_prediction_result():

    global name
    name = request.form.get('name')
    round = request.form.get('round')
    driver_points = request.form.get('driver_points')
    driver_wins = request.form.get('driver_wins')
    driver_position = request.form.get('driver_position')
    constructor_points = request.form.get('constructor_points')
    constructor_wins = request.form.get('constructor_wins')
    constructor_position = request.form.get('constructor_position')
    age = request.form.get('age')


    global finish_position
    finish_position = prediction(name, round, driver_points, driver_position, constructor_points, constructor_position, driver_wins, age, constructor_wins)

    return redirect(url_for('show_result'))

@app.route('/api/show_result')
def show_result():
    return jsonify({'finish_position': finish_position, 'name': name})

if __name__ == '__main__':
    app.run(port=3000)