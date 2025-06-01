# reports/generate_report.py

import os
import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Путь к папкам внутри репо
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_DOCS = os.path.abspath(os.path.join(BASE_DIR, "..", "docs"))
IMAGES_DIR = os.path.join(OUTPUT_DOCS, "images")

# Убедимся, что папка для картинок существует
os.makedirs(IMAGES_DIR, exist_ok=True)

# 1) Сгенерируем какой-то DataFrame и нарисуем график
df = pd.DataFrame({
    "x": range(10),
    "y": [i ** 2 for i in range(10)]
})

# Сохраняем график
plot_path = os.path.join(IMAGES_DIR, "plot.png")
plt.figure(figsize=(5, 4))
plt.plot(df["x"], df["y"], marker="o")
plt.title("Квадратичная зависимость")
plt.xlabel("x")
plt.ylabel("y = x²")
plt.grid(True)
plt.savefig(plot_path)
plt.close()

# 2) Подготовим данные для вставки в шаблон
report_data = {
    "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    "table_html": df.to_html(index=False),
    "plot_path": "images/plot.png",  # относительный путь от docs/
}

# 3) Считываем Jinja2-шаблон и рендерим Markdown
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
template = env.get_template("report_template.md.j2")

rendered_md = template.render(**report_data)

# 4) Сохраняем результат в docs/index.md
output_path = os.path.join(OUTPUT_DOCS, "index.md")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(rendered_md)

print(f"Отчёт сгенерирован: {output_path}")
