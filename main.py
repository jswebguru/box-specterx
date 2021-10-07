import os
from flask import Flask, render_template, request
from boxsdk import OAuth2, Client, BoxAPIException
from settings import CLIENT_ID, CLIENT_SECRET, DEVELOPER_TOKEN

app = Flask(__name__)


@app.route("/box/", methods=['POST'])
def get_meta_data():
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    file_id = request.form['file_id']

    auth = OAuth2(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token=DEVELOPER_TOKEN)
    client = Client(auth)

    try:
        file_info = client.file(file_id).get()
        data_type = file_info.type
        file_name = file_info.name
        file_size = file_info.size
        last_modification_time = file_info.modified_at
        file_owner_name = file_info.owned_by.name
        download_url = client.file(file_id).get_download_url()

        return render_template(
            'home.html',
            data_type=data_type,
            user_name=user_name,
            file_id=file_id,
            file_name=file_name,
            file_size=file_size,
            file_owner_name=file_owner_name,
            last_modification_time=last_modification_time,
            download_url=download_url
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
            file_lists = folder_info.item_collection['entries']
            folder_file_lists = []

            for file_data in file_lists:
                folder_file_id = file_data.id
                folder_file_name = file_data.name
                file_download_url = client.file(folder_file_id).get_download_url()
                folder_file_lists.append({
                    'folder_file_id': folder_file_id,
                    'folder_file_name': folder_file_name,
                    'file_download_url': file_download_url
                })

            return render_template(
                'home.html',
                data_type=data_type,
                folder_id=file_id,
                folder_owner=folder_owner,
                folder_name=folder_name,
                folder_size=folder_size,
                folder_modified_at=folder_modified_at,
                file_lists=folder_file_lists)
    except Exception as e:
        print(e)


@app.route('/api/folder_download/', methods=['POST'])
def file_download():
    folder_id = request.form['folder_id']

    auth = OAuth2(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token=DEVELOPER_TOKEN)
    client = Client(auth)
    folder_info = client.folder(folder_id=folder_id).get()
    file_lists = folder_info.item_collection['entries']
    folder_name = folder_info.name

    current_path = os.path.dirname(os.path.abspath(__file__))
    download_file_folder = os.path.join(current_path, folder_name)
    if not os.path.exists(download_file_folder):
        os.mkdir(download_file_folder)

    for file in file_lists:
        file_id = file.id
        file_name = file.name

        file_content = client.file(file_id).content()
        download_file_name = os.path.join(download_file_folder, file_name)

        with open(download_file_name, 'wb') as f:
            f.write(file_content)
            f.close()

    result = 'Successfully Downloaded!'

    return result


# if __name__ == '__main__':
#     app.run(host='0.0.0.0')
