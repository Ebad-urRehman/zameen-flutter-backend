from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
import pickle
from utils import get_converted_values, abbreviate_number
import numpy as np
from store_db import count_records, fetch_first, query_specific_values

app = Flask(__name__)

df = pd.read_csv('zameen_property_data.csv')

CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    head = df.head()
    head_dict = head.to_json(orient='records')
    return jsonify(head_dict)

@app.route('/api/get_unique', methods=['GET'])
def get_unique():
    col_to_get = ['location', 'city', 'province_name', 'purpose', 'property_type']
    unique_values = {}
    for col in col_to_get:
        unique_values[col] = df[col].unique().tolist()

    unique_values['bedrooms'] = [str(i) for i in range(1,7)]
    unique_values['baths'] = [str(i) for i in range(1,7)]
    print(unique_values)
    return jsonify(unique_values)

@app.route('/api/predict_prices', methods=['POST'])
def predict_prices():
    data = request.get_json()
    
    # loading models
    try:
        with open('model/linear_regression_model.pkl', 'rb') as file:
            regressor = pickle.load(file)
    except FileNotFoundError:
        return {"error": "Pickle file not found!"}, 500
    except Exception as e:
        print(f"Error loading pickle file: {e}")
        return {"error": "Error loading pickle file"}, 500

    with open('model/scaler.pkl', 'rb') as file:
        scaler = pickle.load(file)

    


    num_data = get_converted_values(data['area'], data['area_type'], data['baths'], 
                         data['bedrooms'], data['location'], data['city'], data['property_type'],
                         data['purpose'], data['province_name'])

    scaled_data = scaler.transform([num_data])


    # predicting prices
    prediction = regressor.predict(scaled_data)
    
    # getting real value
    prediction = np.exp(prediction[0])
    prediction = np.exp(prediction)
    
    abbreviate_num = abbreviate_number(prediction)
    result = {'predicted_price' : str(int(prediction)), 'abb' :abbreviate_num}

    return jsonify({'success' : result})


@app.route('/api/fetch_recommendations', methods=['GET'])
def fetch_recommendations():
    data = fetch_first(10)
    return jsonify({'success': data})


@app.route('/api/query', methods=['POST'])
def apply_query():
    query_parameters = request.get_json()
    
    data = query_parameters['data']
    current_page = query_parameters['page_no']
    
    col = list(data.keys())
    print(col)
    limit = 100
    offset = (current_page - 1) * limit

    result, total_records = query_specific_values(col, data, limit, offset)

    # total_records = count_records(col, data)
    total_pages = total_records // limit + 1

    return jsonify({'success': result, 'total_pages': total_pages, 'total_results': total_records})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)