import os.path
import sys
import webbrowser
import time
import requests

list_filename = sys.argv[1]

dir_name = list_filename.split("_urls.txt")[0]
if not os.path.isdir(os.path.join("data", dir_name)):
    os.makedirs(os.path.join("data", dir_name), exist_ok=True)

with open(list_filename, "r") as f:
    url_list = f.read().split("\n")
    count_i = 0
    for i, url in enumerate(url_list):
        webbrowser.open_new_tab(url)
        
        #if count_i % 100 == 0:
        #    time.sleep(5) # pause 5s every 100 it to avoid rate limiting.
        
        # Insert Username & Password for https://urs.earthdata.nasa.gov
        username = "<< USERNAME >>"
        password = "<< PASSWORD >>"

        filename = list(reversed(url.split("/")))[0]

        target_filepath = os.path.join("data", dir_name, filename)

        perc_ = i / len(url_list)
        percentage = '{percent:.2%}'.format(percent=perc_)

        if not os.path.isfile(target_filepath):
            count_i += 1
            with requests.Session() as session:
                session.auth = (username, password)

                print(f"[ {i}/{len(url_list)} - {percentage} ] getting file: {filename}", end='')
                r1 = session.request('get', url)
                r = session.get(r1.url, auth=(username, password))
                if r.ok:
                    print("  saving file...", end='')
                    with open(target_filepath, "wb") as target_file:
                        target_file.write(r.content)
                    print("ok")
        else:
            print(f"[ {i}/{len(url_list)} - {percentage} ] skipping file: {os.path.basename(target_filepath)}")