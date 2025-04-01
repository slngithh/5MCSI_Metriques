from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                 
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
    
    # Count commits per minute
    commit_count_per_minute = [0] * 60
    for minute in commit_minutes:
        commit_count_per_minute[minute] += 1
    
    # Create HTML content for the graph
    graph_html = "<h1>Commits per Minute</h1><table border='1'><tr><th>Minute</th><th>Number of Commits</th></tr>"
    for minute, count in enumerate(commit_count_per_minute):
        graph_html += f"<tr><td>{minute}</td><td>{count}</td></tr>"
    graph_html += "</table>"
    
    return graph_html

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})


if __name__ == "__main__":
  app.run(debug=True)
