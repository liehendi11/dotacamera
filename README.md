# Dota camera

Research code for learning-to-rank-based automated dota spectating camera.

DOI: [10.1007/978-981-13-6661-1_12](https://doi.org/10.1007/978-981-13-6661-1_12)

## Requirements

This code was written in Python version 3.7.

## Content

* `letor_y/` - Result after running the learning-to-rank model. This
  contains tab-separated value of tick, hero number, and Normalized
  Discounted Cumulative Gain (NDCG).
* `resources/` - Contains useful resources for running the script, such
  as name mapping, list of modifiers, and list of missing heroes.
* `assisted_camera_based.py` - Script to run visual testing of result in
  `letor_y/` directory. This works by mimicing keyboard press, so initial
  setup that maps the key press to hero number is required.
* `dota2_flask_server.py` - Flask server that pull the required data from
  GSI (Game State Integration).
* `dota_constants.py` - Maps the dota constants to GSI naming
* `entities.py` - Contains classes for dota entities such as roshan,
  tower, etc.
* `events.py` - Contains classes to parse dota events to its weight.
  This is used to label the data (higher values means the event is
  more important)
* `live_*.py` - Script to parse the live data to appropriate files, such
  as combat log.
* `parser.py` - Script to parse the logs to spreadsheet
* `letor_model_visual_test.ipynb` - Result validation notebook