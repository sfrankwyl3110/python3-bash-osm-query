import os
import requests
from dotenv import load_dotenv

load_dotenv('.env')

api_host = os.getenv('API_BASE')
api_prot = os.getenv('API_PROT')
api_port_elevation = os.getenv('API_ELEVATION_PORT')


def parse_elevation_result(json_dict: dict):
    elevation_results = []
    if "results" in json_dict:
        results = json_dict.get('results')
        for result in results:
            if "elevation" in result:
                if result.get('elevation') is not None:
                    elevation_results.append(result.get('elevation'))
    if elevation_results is not None and len(elevation_results) > 0:
        return elevation_results
    return None


def query_dataset(dataset, lat, lon):
    r_elevation = requests.get(url=f"{api_prot}://{api_host}:{api_port_elevation}/v1/{dataset}?locations={lat},{lon}")
    r_json: dict = r_elevation.json()
    return r_json


def create_elevation_result(dataset, lat, lon):
    elevation_json = query_dataset(dataset, lat, lon)
    elevation_result_parsed = parse_elevation_result(elevation_json)
    if elevation_result_parsed is not None:
        return elevation_result_parsed[0]
    return None


def query_elevation(lat: float, lon: float):
    results = []
    # curl localhost:8858/v1/srtm30m?locations=0.3803307,17.3933595

    datasets = ["srtm30m", "srtm90m", "eudem"]
    for ds in datasets:
        ds_result = create_elevation_result(ds, lat, lon)
        if ds_result is not None:
            results.append(ds_result)

    if len(results) > 0:
        print(f"elevation: {results[0]}")
        return results[0]
