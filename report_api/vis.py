from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import random

def get_past_day(days):
  return relativedelta(days=+days)

def get_past_week(weeks):
  return relativedelta(weeks=+weeks)

def get_past_month(months):
  return relativedelta(months=+months)

def get_past_year(years):
  return relativedelta(years=+years)

def get_past_date(unit, duration):
  if unit == 'year':
    return get_past_year(duration)
  elif unit == 'month':
    return get_past_month(duration)
  elif unit == 'week':
    return get_past_week(duration)
  else:
    return get_past_day(duration)

def get_calendar(food_diary, unit, duration):

  # 1. Calculate the current date
  current_date = datetime.now()
  # 2. Subtract interval/range e.g. subtract 3 weeks from today
  past_date = get_past_date(unit, duration)
  # 3. Calculate the number of days in the interval
  delta = current_date - past_date
  num_days = delta.day
  # 4. Create list to contain all dates
  calendar = []
  # 5. Initialise each element as a dict:
  for delta in range(num_days + 1):
    calendar_date = current_date - relativedelta(days=+delta)
    calendar_day = {
      'x': int(calendar_date.timestamp() * 1000),
      'y': 0
    }
    calendar.append(calendar_day)

  food_diary_mapping = dict({})

  for diary in food_diary:
    # 6. Iterate over the food diary
    # 6.1 Calculate the difference between food diary entry DAY and current DAY
    diary_timestamp = diary['date']
    diary_date = datetime.fromtimestamp(diary_timestamp)
    # 6.2 The difference is the index of the entry in the list
    # delta = datetime.now() - diary_date
    delta = current_date - diary_date
    idx = delta.days
    # 6.3 Update the calorieTotal i.e. y
    calendar[idx]['y'] += diary['total_calories']
    # 6.4 Store the food diary entry in a JS dict where key = date
    day_key = f"{diary_date.day}/{diary_date.month}/{diary_date.year}"
    if not day_key in food_diary_mapping:
      food_diary_mapping[day_key] = []
    food_diary_mapping[day_key].append(diary)

  # 7. Reverse the list to reflect chronological sequence
  calendar = calendar[::-1]
  return calendar

def nutrient_info(food_diary):

  filtered_nutrients = [
    'Carbs',
    'Fiber',
    'Protein',
    'Fat',
    'Calcium',
    'Sugars',
    'Cholesterol',
    'Iron',
    "Vitamin C",
    "Sodium",
    "Saturated",
    "Potassium",
    "Magnesium"
  ]

  nutrient_calories = dict({})

  # Aggregate total calories consumed per nutrient
  for food in food_diary:
    for nutrient in food['nutrients']:
      if nutrient['nutrient_name'] in filtered_nutrients:
        if not nutrient['nutrient_name'] in nutrient_calories:
          nutrient_calories[nutrient['nutrient_name']] = 0
        nutrient_calories[nutrient['nutrient_name']] += nutrient['nutrient_amount']

  return zip(*[ (nutrient, nutrient_calories[nutrient])
                        for nutrient in nutrient_calories ])































# end
