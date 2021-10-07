from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('home.html')


@app.route("/api/get_data/", methods=['POST'])
def get_result():
    file_id = '123456'
    user_id = '456789'

    result = {'file_id': file_id, 'user_id': user_id}

    return result


@app.route("/gdrive/", methods=['Get'])
def get_meta_data():
    data = request

    return data


# if __name__ == '__main__':
#     app.run(host='0.0.0.0')
