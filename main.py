import job_manager as jm_manager

def process_job():
    for number in range(10000):
        print(number)

jmanager = jm_manager.JobManager()
jmanager.add_job("1")

while(True):
    aVal = ""