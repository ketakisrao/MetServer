from flask import Flask, request, jsonify, abort
import pandas as pd
import csv
# import json

my_awesome_app = Flask(__name__)

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

  return jsonify(data)

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

  return jsonify(data)

if __name__ == '__main__':
    my_awesome_app.run()
