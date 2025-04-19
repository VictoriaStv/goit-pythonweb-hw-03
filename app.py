from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
from pathlib import Path

app = Flask(__name__, static_folder='static')
DATA_FILE = Path("storage/data.json")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form.get('username')
        msg = request.form.get('message')
        timestamp = str(datetime.now())

        if username and msg:
            if not DATA_FILE.exists():
                DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
                DATA_FILE.write_text('{}')

            with DATA_FILE.open('r+', encoding='utf-8') as f:
                data = json.load(f)
                data[timestamp] = {'username': username, 'message': msg}
                f.seek(0)
                json.dump(data, f, indent=2)
        return redirect(url_for('read'))
    return render_template('message.html')


@app.route('/read')
def read():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            messages = json.load(f)
    else:
        messages = {}
    return render_template('read.html', messages=messages)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)

