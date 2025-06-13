import os
import json
import matplotlib.pyplot as plt

# 设置根目录
root_dir = "results"

# 存储结构：{model_name: {thinking_time: accuracy}}
data = {}

# 遍历每个推理时间目录，例如 s1_512, s1_1024, ...
for folder in sorted(os.listdir(root_dir)):
    folder_path = os.path.join(root_dir, folder)
    if not folder.startswith("s1_") or not os.path.isdir(folder_path):
        continue
    thinking_time = int(folder.split("_")[1])
    
    # 遍历该目录下的模型子目录
    for model_name in os.listdir(folder_path):
        model_dir = os.path.join(folder_path, model_name)
        for fname in os.listdir(model_dir):
            if fname.startswith("results") and fname.endswith(".json"):
                with open(os.path.join(model_dir, fname)) as f:
                    result = json.load(f)
                    acc = result["results"]["aime24_nofigures"]["exact_match,none"]
                    if model_name not in data:
                        data[model_name] = {}
                    data[model_name][thinking_time] = acc * 100  # 转为百分比

# 可视化
plt.figure(figsize=(8, 5))
for model_name, scores in data.items():
    x = sorted(scores)
    y = [scores[t] for t in x]
    plt.plot(x, y, marker='o', label=model_name)

plt.title("Accuracy vs Thinking Time on AIME24")
plt.xlabel("Average thinking time (tokens)")
plt.ylabel("Accuracy (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
