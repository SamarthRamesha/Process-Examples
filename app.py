from flask import Flask, render_template, request
import json, os

app = Flask(__name__)
DATA_FILE = 'data.json'
processes = [
    'Rolling', 'Drop Forging', 'Press Forging', 'Upset Forging',
    'Extrusion', 'Wire Drawing', 'Sheet Drawing'
]

data = {}
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
else:
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def get_existing_pairs():
    return {(item['material'].lower(), item['product'].lower())
            for entries in data.values() for item in entries}

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        srn = request.form['srn'].strip().upper()
        if srn in data:
            return render_template('form.html', message=f"{srn} already submitted.")

        entries = []
        for i in range(7):
            material = request.form.get(f'material{i}', '').strip()
            product = request.form.get(f'product{i}', '').strip()
            if (material.lower(), product.lower()) in get_existing_pairs():
                return render_template('form.html', message=f"Duplicate: {material} → {product}")
            entries.append({'process': processes[i], 'material': material, 'product': product})

        data[srn] = entries
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)

        return render_template('form.html', message="Thanks for submitting!")

    return render_template('form.html', message='')

@app.route('/view')
def view():
    return render_template('view.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
