from flask import Flask, render_template, request
import pandas as pd
import quad_tournament

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']


        if(not request.values["header_present"]):
            df = pd.read_csv(file, header=None)
        else:
            df = pd.read_csv(file, header="infer")


        rating = df.columns[int(request.values["sort_column_idx"])]
        name = df.columns[int(request.values["name_column_idx"])]

        # quads = QuadTournament(df, name, rating, board_num, request.values["display_sort"], request.values["must_sort"])
        # quads.make_pairing_sheets()
        
        return f'Uploaded: {file.filename}'
    return render_template('index.html')

@app.route('/quad')
def quad():
    return render_template('quad.html')


@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['user_input']
    return f"You entered: {user_input}"


if __name__ == '__main__':
    app.run(debug=True)

