# 👽 外星人入侵 (Alien Invasion) 实验项目

**基于 Python Pygame 库，采用面向对象设计 (OOP) 和 JSON 持久化实现的高级版本。**

---

## ✨ 核心特性与实验目标 Features

| 功能模块 | 描述 | 关键文件 |
|----------|------|----------|
| **💥 爆炸动画计时** | 外星人被击中后，切换到爆炸图像，并在精确的 **`250ms` (可配置)** 延迟后才从游戏精灵组中移除。 | `alien.py`, `settings.py` |
| **💾 最高分持久化** | 游戏统计数据 (`high_score`) 通过 `json` 模块保存到 `high_score.json` 文件中，确保数据持久性。 | `game_stats.py` |
| **🔄 重置最高分按钮** | 在主菜单界面新增了 **“Reset High Score”** 按钮，支持玩家清除历史最高分记录。 | `alien_invasion.py`, `button.py` |
| **🔊 游戏音效控制** | 集成并控制射击和爆炸音效，增强用户体验。 | `alien_invasion.py` |
| **📈 难度动态递增** | 随着关卡提升，飞船、子弹、外星人速度和得分值均按比例增长。 | `settings.py` |

---

## 💻 程序架构与实现亮点 (Architecture & Implementation)

| 文件名称 | 职责描述 | 实验修改重点 |
| :--- | :--- | :--- |
| `alien_invasion.py` | 主游戏控制器，处理事件循环和游戏状态。 | 初始化 `pygame.mixer`，加载音效，处理 Reset 按钮和爆炸音效触发。 |
| `game_stats.py` | 统计信息管理。 | **新增 `load_high_score()`, `save_high_score()`, `reset_high_score()` 方法。** |
| `alien.py` | 外星人 Sprite 类。 | **新增 `exploding` 状态和 `explosion_time` 属性**，实现基于 `time.time()` 的毫秒级计时逻辑。 |
| `settings.py` | 游戏配置。 | 新增 `self.explosion_duration_ms = 250` 配置项。 |
| `button.py` | 按钮渲染和定位。 | `__init__` 中新增 `y_offset` 参数，用于定位 Play 和 Reset 按钮。 |

---

## 🚀 运行环境与方法（Run）

### 1. 依赖安装

本项目基于 Python 3.x，需要安装 Pygame 库：

```bash
pip install pygame
