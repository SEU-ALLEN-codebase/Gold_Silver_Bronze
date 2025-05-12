import csv

from utils.neuron_quality import DistanceEvaluation

import os
import traceback
from tqdm import tqdm

single_dir = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\pipeline_draw\output'
auto_data_dir = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\synthetic_human_auto_swc'
bronze_dir = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\bronze_standard_15_no_attachment'
silver_dir = r"Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\silver_standard_15_no_attachment"
# gold_dir = r"Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\gold_standard_collaborate_modified"
gold_dir = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\gold_standard_15_no_attachment'
ground_truth_dir = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\synthetic_human_swc'

def single_dir_compare():
    de = DistanceEvaluation(2.5)
    data = []
    gold_file_dict = {}
    ground_file_dict = {}
    for file in os.listdir(gold_dir):
        if file.endswith("swc"):
            parts = file.split("_")
            image = parts[0]
            # dotIndex = file.index(".")
            # neuron = file[0:dotIndex]
            gold_file_dict[image] = os.path.join(gold_dir, file)
    for file in os.listdir(ground_truth_dir):
        if file.endswith("swc"):
            parts = file.split("_")
            image = parts[0]
            # dotIndex = file.index(".")
            # neuron = file[0:dotIndex]
            ground_file_dict[image] = os.path.join(ground_truth_dir, file)

    for key in gold_file_dict.keys():
        gold_ground_metrics = de.run(gold_file_dict.get(key), ground_file_dict.get(key))
        data.append({"name": gold_file_dict.get(key).split("\\")[-1],
                     "gold_precision": 1 - gold_ground_metrics[2, 0],
                     "gold_recall": 1 - gold_ground_metrics[2, 1],
                     "gold_F1": 2 * (1 - gold_ground_metrics[2, 0]) * (1 - gold_ground_metrics[2, 1]) / (
                                 2 - gold_ground_metrics[2, 0] - gold_ground_metrics[2, 1])})
    return data

def main():
    auto_data_dict, bronze_file_dict, silver_file_dict, gold_file_dict, ground_file_dict = {}, {}, {}, {}, {}
    for file in os.listdir(auto_data_dir):
        if file.endswith("swc"):
            parts = file.split("_")
            image = parts[0]
            # dotIndex = file.index(".")
            # neuron = file[0:dotIndex]
            auto_data_dict[image] = os.path.join(auto_data_dir, file)
            # auto_data_dict[neuron] = os.path.join(auto_data_dir, file)
    for file in os.listdir(bronze_dir):
        if file.endswith("swc"):
            parts = file.split("_")
            image = parts[0]
            # dotIndex = file.index(".")
            # neuron = file[0:dotIndex]
            bronze_file_dict[image] = os.path.join(bronze_dir, file)
            # bronze_file_dict[neuron] = os.path.join(bronze_dir, file)
    for file in os.listdir(silver_dir):
        if file.endswith("swc"):
            parts = file.split("_")
            image = parts[0]
            # dotIndex = file.index(".")
            # neuron = file[0:dotIndex]
            silver_file_dict[image] = os.path.join(silver_dir, file)
            # silver_file_dict[neuron] = os.path.join(silver_dir, file)
    for file in os.listdir(gold_dir):
        if file.endswith("swc"):
            parts = file.split("_")
            image = parts[0]
            # dotIndex = file.index(".")
            # neuron = file[0:dotIndex]
            gold_file_dict[image] = os.path.join(gold_dir, file)
            # gold_file_dict[neuron] = os.path.join(gold_dir, file)
    for file in os.listdir(ground_truth_dir):
        if file.endswith("swc"):
            parts = file.split("_")
            image = parts[0]
            # dotIndex = file.index(".")
            # neuron = file[0:dotIndex]
            ground_file_dict[image] = os.path.join(ground_truth_dir, file)
            # ground_file_dict[neuron] = os.path.join(ground_truth_dir, file)

    de = DistanceEvaluation(2.5)
    data = []
    for key in gold_file_dict.keys():
        auto_ground_metrics = de.run(auto_data_dict.get(key), ground_file_dict.get(key))
        bronze_ground_metrics = de.run(bronze_file_dict.get(key), ground_file_dict.get(key))
        silver_ground_metrics = de.run(silver_file_dict.get(key), ground_file_dict.get(key))
        gold_ground_metrics = de.run(gold_file_dict.get(key), ground_file_dict.get(key))
        data.append({"name": gold_file_dict.get(key).split("\\")[-1],
                     "auto_data_precision": 1 - auto_ground_metrics[2, 0],
                     "bronze_precision": 1 - bronze_ground_metrics[2, 0],
                     "silver_precision": 1 - silver_ground_metrics[2, 0],
                     "gold_precision": 1 - gold_ground_metrics[2, 0],
                     "auto_data_recall": 1 - auto_ground_metrics[2, 1],
                     "bronze_recall": 1 - bronze_ground_metrics[2, 1],
                     "silver_recall": 1 - silver_ground_metrics[2, 1],
                     "gold_recall": 1 - gold_ground_metrics[2, 1],
                     "auto_data_F1": 2 * (1 - auto_ground_metrics[2, 0]) * (1 - auto_ground_metrics[2, 1]) / (2 - auto_ground_metrics[2, 0] - auto_ground_metrics[2, 1]),
                     "bronze_F1": 2 * (1 - bronze_ground_metrics[2, 0]) * (1 - bronze_ground_metrics[2, 1]) / (2 - bronze_ground_metrics[2, 0] - bronze_ground_metrics[2, 1]),
                     "silver_F1": 2 * (1 - silver_ground_metrics[2, 0]) * (1 - silver_ground_metrics[2, 1]) / (2 - silver_ground_metrics[2, 0] - silver_ground_metrics[2, 1]),
                     "gold_F1": 2 * (1 - gold_ground_metrics[2, 0]) * (1 - gold_ground_metrics[2, 1]) / (2 - gold_ground_metrics[2, 0] - gold_ground_metrics[2, 1])})
    return data

if __name__ == '__main__':
    data = main()
    # data = main()
    # # 指定 CSV 文件的路径
    # csv_file = "eval_human_12_add.csv"
    # data = single_dir_compare(single_dir)
    csv_file = "15_synthetic_eval.csv"

    # 获取字典的键作为 CSV 文件的表头
    fieldnames = data[0].keys()

    # 写入 CSV 文件
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # 写入表头
        writer.writeheader()
        # 写入数据
        writer.writerows(data)
