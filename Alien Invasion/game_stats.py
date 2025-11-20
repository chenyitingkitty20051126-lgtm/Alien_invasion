import json
import os 

class GameStats:
    """跟踪游戏统计信息，并实现最高分的持久化。"""

    def __init__(self, ai_game):
        """初始化统计信息。"""
        self.settings = ai_game.settings
        self.reset_stats()
        
        # 确定最高分文件的路径
        self.filename = 'high_score.json'
        
        # 在游戏开始时加载最高分
        self.high_score = self.load_high_score()

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息。"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        """从文件中加载最高分，如果文件不存在或读取失败则返回 0。"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    # 读取最高分并返回
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                # 文件内容损坏或文件找不到时，返回默认值 0
                return 0
        else:
            # 文件不存在，返回默认值 0
            return 0

    def save_high_score(self):
        """将最高分保存到文件。"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.high_score, f)
        except Exception as e:
            print(f"Error saving high score: {e}")

    def reset_high_score(self):
        """将最高分设置为 0 并保存到文件。"""
        self.high_score = 0
        self.save_high_score() # 立即将重置后的 0 写入文件