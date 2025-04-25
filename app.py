import json
import os
from flask import Flask, render_template, request

app = Flask(__name__)

DATA_FILE = 'data.json'

# Function to read data from the JSON file
def read_data():
    try:
        if not os.path.exists(DATA_FILE):
            print(f"Warning: {DATA_FILE} not found, initializing empty list.")
            return []
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"FileNotFoundError: {DATA_FILE} not found.")
        return []
    except json.JSONDecodeError:
        print("Error: The data file is corrupted or empty.")
        return []
    except Exception as e:
        import traceback
        traceback.print_exc()
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
            srn = request.form['srn']
            materials = [request.form[f'material{i}'] for i in range(7)]
            products = [request.form[f'product{i}'] for i in range(7)]
            
            # Read existing data
            data = read_data()

            # Check for duplicate SRN
            if any(entry['srn'] == srn for entry in data):
                print(f"Duplicate SRN: {srn}")
                return render_template('form.html', message="This SRN has already been entered. Please enter new data.")

            # Append the new entry
            new_entry = {
                'srn': srn,
                'processes': [{'process': process, 'material': material, 'product': product} for process, material, product in zip(
                    ['Rolling', 'Drop Forging', 'Press Forging', 'Upset Forging', 'Extrusion', 'Wire Drawing', 'Sheet Drawing'],
                    materials,
                    products
                )]
            }

            data.append(new_entry)
            write_data(data)

            return render_template('form.html', message="Data submitted successfully!")
        
        except Exception as e:
            print(f"Error during form submission: {e}")
            return render_template('form.html', message="An error occurred during data submission. Please try again.")

    return render_template('form.html')

@app.route("/view")
def view():
    try:
        # Read the data
        data = read_data()
        
        # Flatten the structure to pass to the template
        # This makes it easier to display as rows per SRN
        structured_data = []
        for entry in data:
            srn = entry['srn']
            for process_entry in entry['processes']:
                structured_data.append({
                    'srn': srn,
                    'process': process_entry['process'],
                    'material': process_entry['material'],
                    'product': process_entry['product']
                })

        return render_template('view.html', data=structured_data)

    except Exception as e:
        print(f"Error while reading data for viewing: {e}")
        return render_template('view.html', message="An error occurred while fetching the data.")

if __name__ == "__main__":
    app.run(debug=True)
