import asyncio
import random
from aiohttp import ClientSession
from aiohttp.web_exceptions import HTTPError

BASE_URL = 'http://localhost:5000'
# BASE_URL = 'https://indraabm.pythonanywhere.com/'

MODEL_IDS = [7] * 10

keys = set()
number_of_runs = 0


async def get_model_props(model_id):
    url = f'{BASE_URL}/models/props/{model_id}'
    try:
        async with ClientSession() as session:
            response = await session.get(url=url)
            response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred while fetching props: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    response_json = await response.json()
    exec_key = response_json.get('exec_key').get('val')
    if exec_key in keys:
        print(f'Key already used: {exec_key}')
    keys.add(exec_key)
    print(
        f'Model props fetch:  Exec key {exec_key} | Status - {response.status}')
    return response_json


async def put_model_props(model_id, props):
    url = f'{BASE_URL}/models/props/{model_id}'
    try:
        for key in props:
            prop = props[key]
            if key != 'execution_key' and prop['atype'] == 'INT':
                if key == 'grid_height' or key == 'grid_width':
                    prop['val'] = 10
        async with ClientSession() as session:
            response = await session.put(url=url, json=props)
    except HTTPError as http_err:
        print(f"HTTP error occurred while putting props: {http_err}")
    except Exception as err:
        print(f"An error ocurred: {err}")
    response_json = await response.json()
    exec_key = props.get('exec_key').get('val')
    if response.status == 500:
        print(f'Put props for exec key - {exec_key} was 500.')
    return response_json, response.status


async def run_model(model_id, model):
    count = random.randint(1, 50)
    url = f'{BASE_URL}/models/run/{count}'
    try:
        async with ClientSession() as session:
            response = await session.put(url=url, json=model)
    except HTTPError as http_err:
        print(f"HTTP error occurred while running model: {http_err}")
    except Exception as err:
        print(f"An error ocurred: {err}")
    exec_key = model.get('exec_key')
    print(
        f'Model run status: Exec key {exec_key} | Status - {response.status}')
    response_json = await response.json()
    return response_json


async def run_test(model_id):
    """Wrapper for running program in an asynchronous manner"""
    global number_of_runs
    try:
        response_get_props = await get_model_props(model_id)
        (response_put_props, status) = await put_model_props(model_id,
                                                             response_get_props)
        if status != 500:
            response_run_model = await run_model(model_id, response_put_props)
            number_of_runs += 1

    except Exception as err:
        print(f"Exception occured: {err}")
        pass


def start():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        *[run_test(model_id) for model_id in MODEL_IDS]
    ))
    print(f'Total runs {number_of_runs}\n Total Keys: {len(keys)}')


if __name__ == "__main__":
    start()
