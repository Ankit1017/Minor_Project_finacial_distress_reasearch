from evauation_functions import fitness_function,information_gain
from Bat import*
from movement import update_selected_features
from typing import Iterator
import pandas as pd
from flask import request
import time
import logging
import random
import sys
from datetime import datetime
import json
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
random.seed()
def bat_reduced_data() -> Iterator[str]:
    
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr or ""

    try:
        logger.info("Client %s connected", client_ip)
        data=pd.read_csv(r"D:\mini project\final Submission model\static\Time Series Data\2020_data.csv")
        X = data.iloc[:, 2:-1].values
        y = data.iloc[:, -1].values
        features = list(range(X.shape[1]))
        all_feature_fitness=sum(information_gain(features,X,y))
        population_size = 2
        max_iterations = 10
        pulse_rate = 0.2
        last_bat=[]
        current_bat=[]
        x=[]
        i=0

        # Initialize the population
        population = [Bat(random.sample(features, random.randint(1, len(features))), random.uniform(0, 1), random.uniform(0, 1),X,y) for _ in range(population_size)]

        global_best_solution = None
        best_fitness_counter = 0
        max_best_fitness_counter = 30  # Number of iterations to allow the same best fitness
        ar=[]
        for iteration in range(max_iterations):
            for bat in population:
                fitness = fitness_function(bat.selected_features,X,y)
                
                time.sleep(1)
                ar.append(fitness)
                if fitness > bat.best_fitness:
                    bat.best_selected_features = bat.selected_features
                    bat.best_fitness = fitness

                if global_best_solution is None or fitness > global_best_solution.best_fitness:
                    global_best_solution = bat
                    best_fitness_counter = 0  # Reset the counter
                # else:
                #     best_fitness_counter += 1
                print(bat.selected_features)
                # print("fractional information gain of last bat  : ",(sum(information_gain(bat.selected_features,X,y))/all_feature_fitness))
                kt=((sum(information_gain(bat.selected_features,X,y))/all_feature_fitness))
                new_features = update_selected_features(bat.selected_features,features,X,y)
                print(type(new_features))
                new_features=sorted(new_features)
                print(new_features)
                # print("fractional information gain of new bat  : ",(sum(information_gain(new_features,X,y))/all_feature_fitness))
                ft=((sum(information_gain(new_features,X,y))/all_feature_fitness))
                i+=1
                x.append(i)
                json_data = json.dumps(
                    {
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "value": fitness,
                        "value1":abs(kt-ft),
                        "value2":new_features
                    }
                )
                yield f"data:{json_data}\n\n"
                new_fitness = fitness_function(new_features,X,y)

                if new_fitness > bat.best_fitness or random.random() < pulse_rate:
                    bat.selected_features = new_features

            # Decrease loudness and update frequency for each bat
            for bat in population:
                bat.loudness *= 0.9
                bat.frequency = random.uniform(0, 1) * bat.frequency
    except GeneratorExit:
        logger.info("Client %s disconnected", client_ip)
