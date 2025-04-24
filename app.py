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
    except json.JSONDecodeError:
        # If there is an issue with the JSON format, return an empty list
        print("Error: data.json is empty or has invalid JSON.")
        return []

# Function to write data to the JSON file
def write_data(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error writing data to file: {e}")
        raise

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
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
        
        except Exception as e:
            print(f"Error during form submission: {e}")
            return render_template('form.html', message="An error occurred during data submission. Please try again.")

    return render_template('form.html')

@app.route("/view")
def view():
    try:
        # Read the data from the JSON file
        data = read_data()
        return render_template('view.html', data=data)
    except Exception as e:
        print(f"Error reading data for viewing: {e}")
        return render_template('view.html', message="An error occurred while fetching the data.")

if __name__ == "__main__":
    app.run(debug=True)
