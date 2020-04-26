"""
https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs
"""
import csv
import requests
from flask import Flask, render_template, request, Response 
from bs4 import BeautifulSoup 


app = Flask('jobs')

@app.route('/')
def home():
  return render_template('home.html')

app.run(host="0.0.0.0", debug=True)