import matplotlib.pyplot as plt
import numpy as np

# 原始数据
iterations = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800]
train_loss = [2.6, 2.0, 1.3, 1.4, 0.94, 0.84, 1.1, 0.78, 0.59, 0.75, 0.61, 0.52, 0.59, 0.67, 0.61, 0.59, 0.57, 0.61, 0.49]
val_loss = [2.6, 1.6, 1.4, 1.2, 1.1, 1.0, 1.0, 0.88, 0.86, 0.85, 0.83, 0.82, 0.82, 0.81, 0.8, 0.79, 0.78, 0.79, 0.8]
train_acc = [4.69, 38.28, 58.59, 56.25, 71.88, 75.78, 64.84, 75.0, 82.81, 75.78, 79.69, 84.38, 83.59, 78.12, 78.12, 82.03, 80.47, 82.03, 83.59]
val_acc = [8.9, 46.64, 51.92, 59.92, 66.99, 68.76, 69.83, 72.24, 72.62, 73.5, 74.08, 74.37, 74.47, 74.87, 74.53, 75.56, 75.92, 75.83, 75.6]

# 创建画布和子图
plt.figure(figsize=(14, 6))

# 绘制损失曲线（左轴）
plt.subplot(1, 2, 1)
plt.plot(iterations, train_loss, 'b-', label='Train Loss', linewidth=2)
plt.plot(iterations, val_loss, 'r-', label='Val Loss', linewidth=2)
plt.xlabel('Iterations', fontsize=12)
plt.ylabel('Loss', fontsize=12)
plt.title('Training & Validation Loss', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# 绘制准确率曲线（右轴）
plt.subplot(1, 2, 2)
plt.plot(iterations, train_acc, 'b--', label='Train Acc', linewidth=2)
plt.plot(iterations, val_acc, 'r--', label='Val Acc', linewidth=2)
plt.xlabel('Iterations', fontsize=12)
plt.ylabel('Accuracy (%)', fontsize=12)
plt.title('Training & Validation Accuracy', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# 调整布局并显示
plt.tight_layout()
plt.show()