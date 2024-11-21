import json
import os


def save_to_file(data, filename="config.json"):
    # 如果文件存在，先读取现有数据
    if os.path.exists(filename):
        with open(filename, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = {}

    # 更新数据
    existing_data.update(data)

    # 写回文件
    with open(filename, "w") as f:
        json.dump(existing_data, f, indent=4)


def load_from_file(filename="config.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}
