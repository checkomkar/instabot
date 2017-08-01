from flask import Flask
from flask import jsonify
from flask import request
from cachedSettings import *

api = run_cached()

app = Flask(__name__)

@app.route("/")
def getUserInfo():
	if 'name' in request.args:		
		info = api.username_info(request.args['name'])        
		return jsonify(info)
        
	else:
		info = api.username_info('stratus009')        
		return jsonify(info)
        
    


if __name__ == "__main__":
	app.run()