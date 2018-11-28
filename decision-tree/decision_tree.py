import operator as op
from math import log
DATA_FILE = "lenses.txt"

def load_data(path):
    with open(path, "r") as f:
        lenses = [instance.strip().split("\t") for instance in f.readlines()]
    return lenses

def cal_info_entropy(data):
    label_dict = {}
    for instance in data:
        label = instance[-1]
        label_dict[label] = label_dict.get(label, 0) + 1
    info_entropy = 0.0
    for key in label_dict.keys():
        prob = float(label_dict[key]) / len(data)
        info_entropy -= prob * log(prob, 2)        
    return info_entropy

def split_dataset(data, feature, feature_value):
    feature_data = []
    for data_row in data:
        if data_row[feature] == feature_value:
            new_row = data_row[0 : feature]
            new_row.extend(data_row[feature + 1 :])
            feature_data.append(new_row)
    return feature_data

def choose_best_feature(data):
    feature_num = len(data[0]) - 1
    old_entropy = cal_info_entropy(data)
    best_info_gain = 0.0
    best_feature = -1
    for index in range(feature_num):
        data_list = [instance[index] for instance in data]
        data_set = set(data_list)
        new_entropy = 0.0
        for feature_value in data_set:
            split_data = split_dataset(data, index, feature_value)
            prob = len(split_data) / float(len(data))
            new_entropy += prob * cal_info_entropy(split_data) 
        if old_entropy - new_entropy > best_info_gain:
            best_info_gain = old_entropy - new_entropy
            best_feature = index
    return best_feature           

def true_label(data):
    label_list = {}
    for instance in data:
        label_list[instance] = label_list.get(instance, 0) + 1
    sorted_label = sorted(label_list.items(), key = op.itemgetter(1), reverse = True)
    return sorted_label[0][0]

def create_tree(train_data, features):
    labels = [data_line[-1] for data_line in train_data]
    if labels.count(labels[0]) == len(labels):
        return labels[0]
    
    if len(train_data[0]) == 1:
        return true_label(train_data)
    best_feature_index = choose_best_feature(train_data)
    best_feature = features[best_feature_index]
    my_tree = {best_feature:{}}
    del(features[best_feature_index])
    feature_list = [instance[best_feature_index] for instance in train_data] 
    feature_set = set(feature_list)
    for value in feature_set:
        sub_feature_set = features[:]
        my_tree[best_feature][value] = create_tree(split_dataset(train_data, best_feature_index, value), sub_feature_set)
    return my_tree


def get_tree_dict():
    data = load_data(DATA_FILE)
    features = ['age', 'prescript', 'astigmatic', 'tearRate']
    my_tree = create_tree(data, features)
    return my_tree

if __name__ == "__main__":
    tree = get_tree_dict()
    print(tree)
