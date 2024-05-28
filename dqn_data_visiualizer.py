import json
import time
from dqn_model import Dqn
from data_extractor import get_historical_data
from typing import Iterator
from flask import request
import time
import logging
import random
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
random.seed()
def dqn_based_data(file_path)-> Iterator[str]:
    if request.headers.getlist("X-Forwarded-For"):
            client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr or ""

    try:
        logger.info("Client %s connected", client_ip)
        data=json.loads(get_historical_data(file_path))
        high_values = []
        # print(data)
        for date, values in data.items():
            high_value = values.get('High')
            if high_value and len(high_values)<600:
                high_values.append(values.get("average_price"))
                message = f"Average Price: {values.get('average_price')}"
        yield f"data: {json.dumps({'time': 'N/A', 'message': f'Total high values count: {len(high_values)}', 'average_price': None, 'reward': None, 'total_holds': None, 'total_sells': None})}\n\n"

        brain = Dqn(3, 3, 0.7)

        cash = 100000.0
        stock = 0
        nows = 100000.0
        prev = 100000.0
        l = 0
        i = 0
        a = 1
        o = 0
        z = 0
        ret = []
        st = []

        for j in high_values:
            i += 1
            prev = nows
            nows = nows + (j - l) * stock
            rew = nows - prev
            if a == 0:
                if stock > 0:
                    cash += j
                    stock -= 1
                else:
                    rew = -100    
            if a == 2:
                if cash > j:
                    stock += 1
                    cash -= j
                else:
                    rew = -100       
            if rew > 0:
                rew = 1
            if rew <= 0:
                rew = -1      
            a = brain.update(rew, [j - l, stock, cash])
            l = j

            message = f"Reward: {rew}"
            yield f"data: {json.dumps({'time': i, 'message': message, 'average_price': j, 'reward': rew, 'total_holds': o, 'total_sells': z})}\n\n"
            time.sleep(0.1)

            ret.append(rew)
            st.append(i)
            if rew == -1:
                z += 1
            elif rew == 1:
                o += 1       

        yield f"data: {json.dumps({'time': 'N/A', 'message': f'Total buys: {o}', 'average_price': None, 'reward': None, 'total_holds': o, 'total_sells': None})}\n\n"
        yield f"data: {json.dumps({'time': 'N/A', 'message': f'Total sells: {z}', 'average_price': None, 'reward': None, 'total_holds': None, 'total_sells': z})}\n\n"
        if o>z:
            yield f"data: {json.dumps({'time': 'N/A', 'message': 'Company doesnt suffer a financial Distress', 'average_price': None, 'reward': None, 'total_holds': o, 'total_sells': None})}\n\n"
            yield f"data: {json.dumps({'time': 'N/A', 'message': f'You can buy this!!!', 'average_price': None, 'reward': None, 'total_holds': o, 'total_sells': None})}\n\n"
        else:
            yield f"data: {json.dumps({'time': 'N/A', 'message': f'Company suffers a financial Distress', 'average_price': None, 'reward': None, 'total_holds': o, 'total_sells': None})}\n\n"
            yield f"data: {json.dumps({'time': 'N/A', 'message': f'You must sell this!!!', 'average_price': None, 'reward': None, 'total_holds': o, 'total_sells': None})}\n\n"
        time.sleep(100000)
    except GeneratorExit:
        logger.info("Client %s disconnected", client_ip)
