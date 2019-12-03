from flask import Flask, request, jsonify, abort, current_app, response
import pandas as pd
import csv
import json
import os

my_awesome_app = Flask(__name__)

class_groups = ["China", "Europe", "Greece", "Islam", "Japan", "Oceania"]

@my_awesome_app.route('/')
def hello_world():
    return 'Hello hello hello'

# Returns all rows with artist last name
@my_awesome_app.route('/timeline')
def timeline():

  artist = request.args.get('artist')

  if artist is None: 
    abort(404)
  
  data = {"results": []}
  with open('./data/timelines/' + artist + ".csv") as csvFile:
    reader = csv.DictReader(csvFile)
    for row in reader:
      data["results"].append(row)


  resp = make_response(jsonify(data))
  resp.headers['Access-Control-Allow-Origin'] = '*'

  return resp

# Returns all country counts
@my_awesome_app.route('/country-counts')
def countryCounts():

  data = {"results": []}
  with open("./data/map/geo_count.csv") as csvFile:
    reader = csv.DictReader(csvFile)
    for row in reader:
      data["results"].append(row)

  resp = make_response(jsonify(data))
  resp.headers['Access-Control-Allow-Origin'] = '*'

  return resp

# Returns counts of num artworks per distinct date
# for an artist
@my_awesome_app.route('/timeline-dates')
def timelineDates():
  
  artist = request.args.get('artist')

  if artist is None: 
    abort(404)
  
  df = pd.read_csv('./data/timelines/' + artist + ".csv")
  new_df = df[['Object End Date','Object Number']]
  new_df = new_df.drop_duplicates().groupby('Object End Date').count()
  new_df.columns = ["Date Count"]

  data = new_df.to_dict()

  resp = make_response(jsonify(data))
  resp.headers['Access-Control-Allow-Origin'] = '*'

  return resp

@my_awesome_app.route('/counts-by-date')
def countsByDate():

  dynasty = request.args.get('dynasty')

  if dynasty is None: 
    abort(404)

  SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
  json_url = os.path.join(SITE_ROOT, "data/spiral", dynasty+"-result.json")
  data = json.load(open(json_url))
  resp = make_response(data)
  resp.headers['Access-Control-Allow-Origin'] = '*'

  return resp
#   return data

@my_awesome_app.route('/classification')
def classification():

  id = request.args.get('id')

  if id is None: 
    abort(404)

  id = int(id)
  SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
  
  json_url = os.path.join(SITE_ROOT, "data/classification", class_groups[id-1] + ".json")
  data = json.load(open(json_url))

  resp = make_response({"result": data})
  resp.headers['Access-Control-Allow-Origin'] = '*'

  return resp
#   return {"result": data}

if __name__ == '__main__':
    my_awesome_app.run(debug=True)
