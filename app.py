from flask import Flask
import job_manager as jm_manager
import json as js

app = Flask(__name__)

jmanager = jm_manager.JobManager()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/add/<job_id>')
def add_job(job_id):
    jmanager.add_job(job_id)
    return "success"


@app.route('/addcrazy/<job_id>')
def add_crazy(job_id):
    jmanager.add_crazy(job_id)
    return "success"


@app.route('/addlow/<job_id>')
def add_low(job_id):
    jmanager.add_low_usage_job(job_id)
    return "success"


@app.route('/all')
def all_jobs():
    job_names = jmanager.get_all_jobs()
    js_ret = js.dumps(job_names)
    return js_ret


@app.route('/remove/<job_id>')
def remove_job(job_id):
    jmanager.remove_job(job_id)
    return "success"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
