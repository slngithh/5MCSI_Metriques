from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests
from collections import Counter
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/contact/')
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route('/rapport/')
def mongraphique():
    return render_template('graphique.html')

@app.route('/histogramme/')
def histo():
    return render_template('histogramme.html')

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

@app.route('/commits/')
def show_commit_graph():
    url = "https://api.github.com/repos/slngithh/5MCSI_Metriques/commits"
    response = requests.get(url)

    if response.status_code != 200:
        return f"Erreur de récupération des données: {response.status_code}", 500

    commits = response.json()
    minute_counts = Counter()

    for commit in commits:
        try:
            date_str = commit['commit']['author']['date']
            minute = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ').minute
            minute_counts[minute] += 1
        except Exception as e:
            continue  # En cas d'erreur sur un commit, on saute
    minutes = list(range(60))
    counts = [minute_counts.get(minute, 0) for minute in minutes]

    return render_template('commits.html', labels=minutes, values=counts)

if __name__ == "__main__":
  app.run(debug=True)
