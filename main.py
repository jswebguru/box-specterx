from flask import Flask, render_template, request
import requests

app = Flask(__name__)

result = []


@app.route("/")
def hello():
    return render_template('home.html')


@app.route("/api/get_data/", methods=['POST'])
def get_result():

    return result


@app.route("/gdrive/", methods=['POST'])
def get_meta_data():
    user_id = request.form['user_id']
    file_id = request.form['file_ids']

    result.append({'file_id': file_id, 'user_id': user_id})


# if __name__ == '__main__':
#     app.run(host='0.0.0.0')
