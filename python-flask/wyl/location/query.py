import requests
import os
from urllib.parse import urlparse, parse_qs
from app.constants import Constants
from dotenv import load_dotenv
from wyl.helpers import max_key, reduce_dict_by_keys, list_to_csl

load_dotenv('.env')

api_prot = os.getenv('API_PROT')
api_base = os.getenv('API_BASE')
api_port = os.getenv('API_PORT')


def query_location(query_location_param: str) -> dict:
    request_url = f"{api_prot}://{api_base}:{api_port}?q={query_location_param}"

    session = requests.session()

    keys_to_keep = Constants.keys_to_keep

    try:
        r_head = session.head(url=request_url, timeout=10)
        if r_head.status_code == 200:
            r_get = session.get(request_url)

            response_json: dict = r_get.json()

            if len(response_json) == 0:
                print("no results")

            elif len(response_json) > 0:
                max_importance_dict: dict = max_key(response_json, 'importance')
                reduced_dict: dict = reduce_dict_by_keys(max_importance_dict, keys_to_keep)

                tmp_dict = {}
                for k, v in reduced_dict.items():
                    if k == "boundingbox":
                        tmp_dict[k] = list_to_csl(v)
                    else:
                        tmp_dict[k] = v

                parsed = urlparse(request_url)
                qs = parse_qs(parsed.query)
                query = qs.get('q')[0]
                tmp_dict["query"] = query
                return tmp_dict

    except requests.exceptions.ConnectTimeout as connect_timeout:
        for arg in connect_timeout.args:
            print(arg)
