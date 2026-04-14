import matplotlib.pyplot as plt

categories = ["Python", "JavaScript", "Java", "C++", "Go", "Rust"]
values = [85, 78, 65, 55, 45, 40]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(categories, values, color=["#3776AB", "#F7DF1E", "#ED8B00", "#00599C", "#00ADD8", "#DEA584"])

ax.set_title("Programming Language Popularity", fontsize=16, fontweight="bold")
ax.set_xlabel("Language", fontsize=12)
ax.set_ylabel("Popularity Score", fontsize=12)

for bar, value in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(value), ha="center", va="bottom", fontsize=11)

ax.set_ylim(0, 100)
plt.tight_layout()
plt.savefig("barchart.png", dpi=150)
plt.show()
