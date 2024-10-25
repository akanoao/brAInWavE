from flask import Flask, request, render_template, redirect, url_for, jsonify

app = Flask(__name__)

# Initial moisture values
moisture_threshold = 40  
last_checked_moisture = None
message = ""
current_mode = "Basic" 


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route('/')
def home():
    return render_template('home.html')

# Route to display the dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard():
    global moisture_threshold
    global last_checked_moisture
    global message
    global current_mode

    return render_template('dashboard.html', 
                           moisture_threshold=moisture_threshold, 
                           last_checked_moisture=last_checked_moisture,
                           message=message,mode=current_mode)

@app.route('/settings', methods=['GET'])
def settings():
    global moisture_threshold, current_mode
    return render_template('settings2.html', 
                           moisture_threshold=moisture_threshold,
                           current_mode=current_mode)

# Route triggered by the "GET MOISTURE" button
@app.route('/get_moisture', methods=['POST'])
def get_moisture():
    global last_checked_moisture
    global message
    
    # Check if the request contains JSON data (from ESP32)
    if request.is_json:
        data = request.get_json()
        last_checked_moisture = data.get('moisture')  # Get the moisture data
        print(f"Moisture level received: {last_checked_moisture}")
        return jsonify({"status": "Moisture data received"}), 200
    
    # If request is from dashboard (which won't send JSON), just return success
    else:
        print("Dashboard requested moisture data update")
        return redirect(url_for('dashboard'))

@app.route('/update_threshold', methods=['POST'])
def update_threshold():
    global moisture_threshold
    global current_mode
    new_threshold = request.form.get('threshold', type=int)
    if new_threshold is not None:
        if 0 <= new_threshold <= 100:
            moisture_threshold = new_threshold
    
    selected_mode = request.form.get('mode')
    # print(selected_mode)
    if selected_mode in ["Basic", "ML Prediction"]:
        current_mode = selected_mode
        # print(f"\n\n\nUpdated mode: {current_mode}") 
    
    return redirect(url_for('dashboard'))


# @app.route('/update_mode', methods=['POST'])
# def update_mode():
#     global current_mode
#     selected_mode = request.form.get('mode')
#     print(selected_mode)
#     if selected_mode in ["Basic", "ML Prediction"]:
#         current_mode = selected_mode
#         print(f"\n\n\nUpdated mode: {current_mode}")  
#     return redirect(url_for('dashboard'))




@app.route('/water', methods=['GET'])
def water():
    global last_checked_moisture
    global moisture_threshold
    global current_mode  
    global message
    
    if last_checked_moisture is not None:
        
        # Check if mode is Basic
        if current_mode == "Basic":
            if last_checked_moisture < moisture_threshold:
                message = "Moisture is below the threshold. Watering will be initiated."
                return jsonify({"cmd": "water"}), 200
            else:
                message = f"Moisture is {last_checked_moisture}%, which is more than the threshold ({moisture_threshold}%). No watering needed. Next check will be in 60 seconds."
                return jsonify({"cmd": "no_water"}), 200
        
        # Check if mode is ML Prediction
        # elif current_mode == "ML Prediction":
        #     # Call the ML model function to get the decision
        #     ml_decision = predict_watering_action(last_checked_moisture, weather_data, humidity, temperature)
            
        #     if ml_decision == "water":
        #         message = "ML Model suggests watering based on conditions."
        #         return jsonify({"cmd": "water"}), 200
        #     else:
        #         message = "ML Model suggests no watering needed based on conditions."
        #         return jsonify({"cmd": "no_water"}), 200
    
    # If no moisture data is available
    message = "Moisture data not available."
    return jsonify({"cmd": "no_data"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
