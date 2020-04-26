"""
https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs
"""
import csv
import requests
from flask import Flask, render_template, request, Response 
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}

db={}

# 링크, 회사, 타이틀

def scrape_stackoverflow(term):
  jobs=[]
  r= requests.get(f'https://stackoverflow.com/jobs?r=true&q={term}',headers=headers)
  soup = BeautifulSoup(r.text, 'html.parser')
  results = soup.find_all('div', {'class': '-job'})
  for x in results:
    s= x.find('div', {'class': 'fl1'})
    title= s.a.text
    company= s.h3.span.text
    link= f"https://stackoverflow.com{s.a['href']}"
    if title and link and company:
      job = {
            "title": title,
            "link": link,
            "company": company
            }
      jobs.append(job)
  return jobs

def scrape_wework(term):
  jobs=[]
  r= requests.get(f'https://weworkremotely.com/remote-jobs/search?term={term}',headers=headers)
  soup = BeautifulSoup(r.text, 'html.parser')
  results = soup.find_all('li', {'class': 'feature'})
  for x in results:
    title= x.find('span',{'class':'title'}).text
    company= x.find('span',{'class':'company'}).text
    link= x.a.get('href')
    if title and link and company:
      job = {
            "title": title,
            "link": f"https://weworkremotely.com{link}",
            "company": company
            }
      jobs.append(job)
  return jobs

def scrape_remoteok(term):
  jobs=[]
  r= requests.get(f'https://remoteok.io/remote-dev+{term}-jobs',headers=headers)
  soup = BeautifulSoup(r.text, 'html.parser')
  results = soup.find_all('td',{'class':'company_and_position'})
  for x in results:
    title= x.h2.text
    company= x.find('a',{'class':'companyLink'}).h3.text
    link= x.a.get('href')
    if title and link and company:
      job = {
            "title": title,
            "link": f"https://remoteok.io/{link}",
            "company": company
            }
      jobs.append(job)
  return jobs

app = Flask('jobs')

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/search')
def search():
  term = request.args.get('term')
  if not db.get(term):
    db[term] = scrape_remoteok(term)
    db[term].extend(scrape_stackoverflow(term))
    db[term].extend(scrape_wework(term))
  jobs=db[term]
  count= len(jobs)
  return render_template('search.html',jobs=jobs,count=count,term=term)

app.run(host="0.0.0.0", debug=True)