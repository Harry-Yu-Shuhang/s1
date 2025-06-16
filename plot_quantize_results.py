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

for task in tasks:
    data = {}  # {model_name: {thinking_time: acc}}

    for folder in sorted(os.listdir(root_dir)):
        folder_path = os.path.join(root_dir, folder)
        if "_" not in folder or not os.path.isdir(folder_path):
            continue

        try:
            model_name, thinking_time_str = folder.rsplit("_", 1)
            thinking_time = int(thinking_time_str)
        except ValueError:
            continue

        for task_name in os.listdir(folder_path):
            if task_name != task:
                continue

            task_dir = os.path.join(folder_path, task_name)
            if not os.path.isdir(task_dir):
                continue

            for sub_model_dir in os.listdir(task_dir):
                result_root = os.path.join(task_dir, sub_model_dir)
                if not os.path.isdir(result_root):
                    continue

                for result_subdir in os.listdir(result_root):
                    result_dir = os.path.join(result_root, result_subdir)
                    if not os.path.isdir(result_dir):
                        continue

                    for fname in os.listdir(result_dir):
                        if fname.startswith("results") and fname.endswith(".json"):
                            fpath = os.path.join(result_dir, fname)
                            try:
                                with open(fpath) as f:
                                    result = json.load(f)
                                if task not in result["results"]:
                                    print(f"⚠️ {fpath} 中不含任务 {task}")
                                    continue
                                acc = result["results"][task].get("exact_match,none", 0)
                                if model_name not in data:
                                    data[model_name] = {}
                                data[model_name][thinking_time] = acc * 100
                            except Exception as e:
                                print(f"❌ 读取失败 {fpath}: {e}")

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
