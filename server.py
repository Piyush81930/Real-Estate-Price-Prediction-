from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import util
import os

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Serve the main HTML page
@app.route('/')
def home():
    return render_template('app.html')  # Ensure 'app.html' is in the 'templates' folder

# Route to get location names
@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        locations = util.get_location_names()
        response = jsonify({'locations': locations})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return jsonify({'error': 'Failed to load locations', 'details': str(e)}), 500

# Route to predict home price based on input data
@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        # Extract data from form request
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        # Calculate estimated price
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        response = jsonify({'estimated_price': estimated_price})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except KeyError as e:
        return jsonify({'error': f'Missing form parameter: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': 'Prediction failed', 'details': str(e)}), 500

# Load model artifacts and start the server
if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    port = int(os.environ.get('PORT', 10000))  # Get port from environment or default to 5000
    util.load_saved_artifacts()
    app.run(host='0.0.0.0', port=port)

