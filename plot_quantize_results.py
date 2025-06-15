import os
import json
import matplotlib.pyplot as plt

# 根目录和输出目录
root_dir = "results"
output_dir = "quantize_visual_results"
os.makedirs(output_dir, exist_ok=True)

# 支持的任务名列表
tasks = [
    "aime24_nofigures",
    "openai_math",
    "gpqa_diamond_openai"
]

# 遍历每个任务，分别绘图
for task in tasks:
    data = {}  # {model_name: {thinking_time: acc}}

    for folder in sorted(os.listdir(root_dir)):
        folder_path = os.path.join(root_dir, folder)
        if not folder.startswith("s1_") or not os.path.isdir(folder_path):
            continue

        try:
            thinking_time = int(folder.split("_")[1])
        except ValueError:
            continue

        for task_name in os.listdir(folder_path):
            task_dir = os.path.join(folder_path, task_name)
            if task != task_name or not os.path.isdir(task_dir):
                continue

            for model_name in os.listdir(task_dir):
                model_dir = os.path.join(task_dir, model_name)
                if not os.path.isdir(model_dir):
                    continue

                for subdir in os.listdir(model_dir):
                    result_dir = os.path.join(model_dir, subdir)
                    if not os.path.isdir(result_dir):
                        continue

                    for fname in os.listdir(result_dir):
                        if fname.startswith("results") and fname.endswith(".json"):
                            fpath = os.path.join(result_dir, fname)
                            with open(fpath) as f:
                                result = json.load(f)
                                if task not in result["results"]:
                                    continue
                                acc = result["results"][task].get("exact_match,none", 0)
                                if model_name not in data:
                                    data[model_name] = {}
                                data[model_name][thinking_time] = acc * 100

    # 绘图
    if not data:
        print(f"⚠️ No data found for task: {task}")
        continue

    plt.figure(figsize=(8, 5))
    for model_name, scores in sorted(data.items()):
        x = sorted(scores)
        y = [scores[t] for t in x]
        plt.plot(x, y, marker='o', label=model_name)

    task_label = {
        "aime24_nofigures": "Competition Math (AIME24)",
        "openai_math": "Mathematical Problem Solving (MATH500)",
        "gpqa_diamond_openai": "PhD-Level Science Questions (GPQA Diamond)"
    }

    plt.title(f"Accuracy vs Thinking Time\n{task_label.get(task, task)}")
    plt.xlabel("Average thinking time (tokens)")
    plt.ylabel("Accuracy (%)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    save_path = os.path.join(output_dir, f"{task}_accuracy_vs_thinking_time.png")
    plt.savefig(save_path)
    plt.close()

    print(f"✅ Saved plot: {save_path}")