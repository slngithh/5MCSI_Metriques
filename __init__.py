from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import matplotlib.pyplot as plt
import requests
                                                                                                                                       
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

@app.route('/commits')
def commits():
    # Get commits data from GitHub API
    response = requests.get('https://api.github.com/repos/slngithh/5MCSI_Metriques/commits')
    commits_data = response.json()

    # Process commits data to get commit minutes
    commit_minutes = []
    for commit in commits_data:
        date_string = commit['commit']['author']['date']
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        commit_minutes.append(date_object.minute)
    
    # Create a graph of commit activity minute by minute
    plt.hist(commit_minutes, bins=range(0, 61), edgecolor='black')
    plt.xlabel('Minutes')
    plt.ylabel('Number of Commits')
    plt.title('Commits per Minute')
    plt.savefig('static/commits_per_minute.png')
    plt.close()

    return render_template('commits.html')

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})


if __name__ == "__main__":
  app.run(debug=True)
