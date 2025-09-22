from flask import Flask, render_template, request
import random
import sqlite3
import requests

API_KEY = "b3822fc787mshe1a54a8c09d1f0dp111d57jsn44f6265e8fdd"


app = Flask(__name__)

def get_job_listings(job_role, skills, location):
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {
        "query": f"{job_role} {skills} in {location}",
        "page": "1",
        "num_pages": "2"
    }

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        results = []
        for job in data.get("data", [])[:10]:  # top 10 results
            results.append({
                "title": job.get("job_title", "Unknown Title"),
                "company": job.get("employer_name", "Unknown Company"),
                "location": job.get("job_city", "Unknown Location"),
                "description": job.get("job_description", "No description available"),
                "skills": job.get("job_required_skills", "Not specified"),
                "link": job.get("job_apply_link", "#")
            })
        return results
    else:
        return [{"title": "Error fetching jobs", "company": "Error", "location": "", "description": "Error fetching job data", "skills": "", "link": "#"}]
        
def init_db():
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS job_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    job_role TEXT,
                    skills TEXT,
                    location TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        #email = request.form["email"]
        job_role = request.form["job_role"]
        skills = request.form["skills"]
        location = request.form["location"]

        # Save to DB
        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()
        c.execute("INSERT INTO job_requests (name, job_role, skills, location) VALUES (?, ?, ?, ?)",
                  (name, job_role, skills, location))
        conn.commit()
        conn.close()

        # Call job search function
        top_jobs = get_job_listings(job_role, skills, location)

        return render_template("result.html", name=name, jobs=top_jobs)

    return render_template("index.html")


# This second index route was causing the duplicate endpoint error

if __name__ == "__main__":
    app.run(debug=True)
