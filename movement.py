from random import choices
import random
from evauation_functions import information_gain
def item_picker_avoider(items, quantities, num_to_pick, elements_to_avoid):
    filtered_items = [item for item in items if item not in elements_to_avoid]
    filtered_quantities = [quantities[idx] for idx, item in enumerate(items) if item not in elements_to_avoid]
    if not filtered_items:
        return []
    chosen_items = choices(filtered_items, weights=filtered_quantities, k=num_to_pick)
    return chosen_items
def update_selected_features(current_features,features,X,y):
    new_features = current_features.copy()
    k=20
    while k>0:
        if len(new_features) > 1:
            feature_to_remove = random.choice(new_features)
            new_features.remove(feature_to_remove)
        feature_to_add = item_picker_avoider(features,[1 for i in range(len(features))],1,new_features)
        new_features.append(feature_to_add[0])
        k-=1
        if sum(information_gain(current_features,X,y))<sum(information_gain(new_features,X,y)):
            break
        while len(new_features)>20:
            feature_to_remove = random.choice(new_features)
            new_features.remove(feature_to_remove)
    return new_features
