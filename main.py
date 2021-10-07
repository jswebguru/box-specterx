from flask import Flask, render_template, request
from boxsdk import OAuth2, Client, BoxAPIException
from settings import CLIENT_ID, CLIENT_SECRET, DEVELOPER_TOKEN

app = Flask(__name__)


@app.route("/box/", methods=['POST'])
def get_meta_data():
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    file_id = request.form['file_id']

    auth = OAuth2(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        access_token=DEVELOPER_TOKEN,
    )
    client = Client(auth)

    try:
        file_info = client.file(file_id).get()
        data_type = file_info.type
        file_name = file_info.name
        file_size = file_info.size
        last_modification_time = file_info.modified_at
        file_owner_name = file_info.owned_by.name

        return render_template(
            'home.html',
            data_type=data_type,
            user_name=user_name,
            file_name=file_name,
            file_size=file_size,
            file_owner_name=file_owner_name,
            last_modification_time=last_modification_time,
        )
    except BoxAPIException as e:
        status = e.status
        if status == 404:
            folder_info = client.folder(folder_id=file_id).get()
            data_type = folder_info.type
            folder_owner = folder_info.created_by.name
            folder_name = folder_info.name
            folder_size = folder_info.size
            folder_modified_at = folder_info.modified_at
            total_count = folder_info.item_collection['total_count']
            folder_file_lists = []
            for index in range(0, total_count):
                folder_file_info = folder_info.item_collection['entries'][index]
                folder_file_id = folder_file_info.id
                folder_file_name = folder_file_info.name
                folder_file_lists.append({'folder_file_id': folder_file_id, 'folder_file_name': folder_file_name})

            return render_template(
                'home.html',
                data_type=data_type,
                folder_owner=folder_owner,
                folder_name=folder_name,
                folder_size=folder_size,
                folder_modified_at=folder_modified_at,
                file_lists=folder_file_lists)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
