import requests
from os import path
import sqlite3
import config

multimedia_urls = {'audio': config.audio_url, 'image': config.image_url, 'video': config.video_url}

# paths
database_path = config.base_dir+"/multimedia/database.sqlite"


def send_files():
    if path.isfile(database_path):
        conn = sqlite3.connect(database_path, detect_types=sqlite3.PARSE_COLNAMES)
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute("select * from file where transferred=? limit ?",
                       (0, config.TRANS_LIMIT))
        rows = cursor.fetchall()

        if len(rows) == 0:
            print('...No files to send...')
            conn.close()
            return

        print('attempting sending files')

        for row in rows:
            row_dict = dict(row)
            mult_url = multimedia_urls[row_dict['file_type']]
            if mult_url == "":
                print("url for "+row_dict['file_type']+" is blank hence file not transferred.")
                continue

            file = open(row_dict['file_path'], 'rb')
            payload = {'title': row_dict['file_name']}
            files = [(row_dict['file_type'], (row_dict['file_type'], file, 'application/octet-stream'))]
            response = requests.request("POST", config.server_address+mult_url, headers=None, data=payload, files=files)
            file.close()
            if "true" in response.text:
                conn.execute("update file set transferred = 1 where id = ?", (row_dict['id']))
                conn.commit()
                print(row_dict['file_name']+" transferred successfully.")
            else:
                print(row_dict['file_name']+" transfer failed!")
        print('closing.....')
        conn.close()
    else:
        print('No files to send')


if __name__ == "__main__":
    send_files()
