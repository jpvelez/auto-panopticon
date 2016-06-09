import requests
import arrow
import yaml
import csv

def fix_timestamp(timestamp):
    try:
        return int(str(timestamp)[:-3])
    except ValueError:
        return None

def ts_to_date(timestamp):
    return arrow.get(timestamp).to("US/Eastern").format('YYYY-MM-DD HH:mm:ss')

auth = yaml.load(open('auth.yaml', 'r'))
base_url = "https://api.fitty.co/users/jpv/workouts"
params = "?api_key={}&app_token={}".format(auth['api_key'], auth['app_token'])
url = base_url + params
workouts = requests.get(url).json()

writer = csv.writer(open("out.csv", "w"))
writer.writerow(["start_time", "end_time", "exercise_name", "reps", "note"])
for workout in workouts:
    start_time = ts_to_date(fix_timestamp(workout['date']))
    end_time = ts_to_date(fix_timestamp(workout['end_date']))
    note = workout['note']
    for exercise in workout['exercises']:
        exercise_name = exercise.get('label', "None")
        for ex_set in exercise['sets']:
            reps = ex_set['reps']
            writer.writerow([start_time, end_time, exercise_name, reps, note])


