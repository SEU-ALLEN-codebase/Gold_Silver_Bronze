import json
import os

swc_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\synthetic_human_swc'

def parse_swc(swc_file):
    tree = []
    with open(swc_file) as fp:
        for line in fp.readlines():
            line = line.strip()
            if not line: continue
            if line[0] == '#': continue
            idx, type_, x, y, z, r, p = line.split()[:7]
            idx = int(idx)
            type_ = int(type_)
            x = float(x)
            y = float(y)
            z = float(z)
            r = float(r)
            p = int(p)
            tree.append((idx, type_, x, y, z, r, p))

    return tree

def get_root_coor(tree):
    for swc_node in tree:
        p = swc_node[-1]
        if p == -1:
            return swc_node[2], swc_node[3], swc_node[4]

data = []
for swc_name in os.listdir(swc_dir_path):
    parts = swc_name.split("_")
    image = parts[0] + "_synthetic"
    neuron = parts[0] + "_" + parts[1] + "_synthetic"
    swc_path = os.path.join(swc_dir_path, swc_name)
    tree = parse_swc(swc_path)
    x, y, z = get_root_coor(tree)
    dict = {}
    dict["Name"] = neuron
    dict["Image"] = image
    dict["X"] = x
    dict["Y"] = y
    dict["Z"] = z
    data.append(dict)

fileName = "soma_coor.json"

with open(fileName, "w") as json_file:
    json.dump(data, json_file)