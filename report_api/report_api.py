from flask import Flask, request, render_template, url_for, jsonify
from datetime import datetime
from vis import get_calendar, nutrient_info
from sample_req2 import body
import requests
import json

app = Flask(__name__)

colours = ["rgb(244, 75, 66)", "rgb(244, 134, 65)", "rgb(244, 184, 65)", "rgb(244, 238, 65)",
           "rgb(193, 244, 65)", "rgb(65, 244, 127)", "rgb(65, 244, 223)", "rgb(65, 196, 244)",
           "rgb(65, 145, 244)", "rgb(65, 79, 244)", "rgb(106, 65, 244)", "rgb(172, 65, 244)",
           "rgb(244, 65, 127)"]

def convert_display(unit):
  units = ["day", "day", "week", "month", "year"]
  for i in range(1, len(units)):
    if units[i] == unit:
      return units[i-1]
  return "year"

def convert_step(display_unit):
  if display_unit == 'hour':
    return 24
  elif display_unit == 'day':
    return 7
  elif display_unit == 'week':
    return 52
  elif display_unit == 'month':
    return 12
  else:
    return 1



@app.route("/report", methods=['GET'])
def report():
  # Get user details and report constraints
  args = request.args
  user_id = args.get('user_id')
  unit = args.get('unit')
  duration = args.get('duration')

  # Fetch the data from the Java backend
  headers={"Content-Type":"application/json"}
  data = { 'user_id': user_id, 'unit': unit, 'duration': duration }
  r = requests.post("http://127.0.0.1:5001/food_diary", json=data, headers=headers)
  body = json.loads(r.content)

  # Generate report with food diary
  user = body['user']
  unit = body['unit']
  duration = body['duration']
  food_diary = body['food_diary']
  calendar = get_calendar(food_diary, unit, duration)
  nutrient_labels, nutrient_data = nutrient_info(food_diary)
  nutrient_colours = colours[:len(nutrient_labels)]
  display_unit = convert_display(unit)
  display_step = convert_step(display_unit)
  todays_date = datetime.now().strftime("%d/%m/%y")
  return render_template('index.html', name=user, 
                                       dataset=json.dumps(calendar), 
                                       nutrient_labels=json.dumps(nutrient_labels), 
                                       nutrient_data=json.dumps(nutrient_data),
                                       nutrient_colours=json.dumps(nutrient_colours),
                                       display_unit=json.dumps(display_unit),
                                       display_step=display_step,
                                       todays_date=todays_date)

if __name__ == "__main__":
  app.run(port=5000)
