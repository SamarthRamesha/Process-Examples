import json
from flask import Flask, render_template, request

app = Flask(__name__)

# Path to the JSON file where the data is stored
DATA_FILE = 'data.json'

# Function to read data from the JSON file
def read_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Function to write data to the JSON file
def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the SRN and the rest of the form data
        srn = request.form['srn']
        materials = [request.form[f'material{i}'] for i in range(7)]
        products = [request.form[f'product{i}'] for i in range(7)]
        
        # Read the existing data from the JSON file
        data = read_data()

        # Check if the submitted SRN already exists
        for entry in data:
            if entry['srn'] == srn:
                # If SRN exists, show an error message and re-render the form
                return render_template('form.html', message="This SRN has already been entered. Please enter new data.")

        # If the SRN is unique, append the new entry
        new_entry = {
            'srn': srn,
            'processes': [{'process': process, 'material': material, 'product': product} for process, material, product in zip(
                ['Rolling', 'Drop Forging', 'Press Forging', 'Upset Forging', 'Extrusion', 'Wire Drawing', 'Sheet Drawing'],
                materials,
                products
            )]
        }

        data.append(new_entry)

        # Write the updated data back to the JSON file
        write_data(data)

        return render_template('form.html', message="Data submitted successfully!")
    
    return render_template('form.html')

@app.route("/view")
def view():
    # Read the data from the JSON file
    data = read_data()
    return render_template('view.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
