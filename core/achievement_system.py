import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class AchievementSystem:
    """成就系统，跟踪用户在各个游戏和计算器中的成就"""

    def __init__(self, data_dir: str = "data"):
        """初始化成就系统"""
        self.data_dir = data_dir
        self.achievements_file = os.path.join(data_dir, "achievements.json")

        # 确保数据目录存在
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # 初始化成就定义
        self.achievement_definitions = self._define_achievements()

        # 加载或初始化成就数据
        self.achievements = self._load_achievements()

        # 当前用户进度统计
        self.stats = {
            "calculator_uses": 0,
            "calculator_total_operations": 0,
            "twentyfour_games_played": 0,
            "twentyfour_games_won": 0,
            "snake_games_played": 0,
            "snake_high_score": 0,
            "tetris_games_played": 0,
            "tetris_high_score": 0,
            "quickmath_games_played": 0,
            "quickmath_correct_answers": 0
        }

        # 加载统计数据
        self._load_stats()

    def _define_achievements(self) -> Dict[str, Dict]:
        """定义所有可能的成就"""
        return {
            # 计算器相关成就
            "calc_beginner": {
                "title": "计算新手",
                "description": "完成10次计算",
                "category": "calculator",
                "icon": "🔢",
                "threshold": 10,
                "stat": "calculator_total_operations"
            },
            "calc_pro": {
                "title": "计算高手",
                "description": "完成100次计算",
                "category": "calculator",
                "icon": "🧮",
                "threshold": 100,
                "stat": "calculator_total_operations"
            },
            "calc_master": {
                "title": "计算大师",
                "description": "完成1000次计算",
                "category": "calculator",
                "icon": "🏆",
                "threshold": 1000,
                "stat": "calculator_total_operations"
            },

            # 二十四点游戏成就
            "twentyfour_first_win": {
                "title": "首胜！",
                "description": "第一次解决二十四点问题",
                "category": "twentyfour",
                "icon": "🥇",
                "threshold": 1,
                "stat": "twentyfour_games_won"
            },
            "twentyfour_50_wins": {
                "title": "二十四点达人",
                "description": "解决50个二十四点问题",
                "category": "twentyfour",
                "icon": "🌟",
                "threshold": 50,
                "stat": "twentyfour_games_won"
            },

            # 贪吃蛇游戏成就
            "snake_first_game": {
                "title": "蛇的诞生",
                "description": "第一次玩贪吃蛇游戏",
                "category": "snake",
                "icon": "🐍",
                "threshold": 1,
                "stat": "snake_games_played"
            },
            "snake_100_score": {
                "title": "蛇的成长",
                "description": "贪吃蛇游戏中获得100分",
                "category": "snake",
                "icon": "📈",
                "threshold": 100,
                "stat": "snake_high_score"
            },

            # 俄罗斯方块游戏成就
            "tetris_first_game": {
                "title": "方块入门",
                "description": "第一次玩俄罗斯方块游戏",
                "category": "tetris",
                "icon": "🧱",
                "threshold": 1,
                "stat": "tetris_games_played"
            },

            # 速算挑战成就
            "quickmath_10_correct": {
                "title": "速算小能手",
                "description": "速算挑战中获得10个正确答案",
                "category": "quickmath",
                "icon": "⚡",
                "threshold": 10,
                "stat": "quickmath_correct_answers"
            },
            "quickmath_100_correct": {
                "title": "速算大师",
                "description": "速算挑战中获得100个正确答案",
                "category": "quickmath",
                "icon": "🏅",
                "threshold": 100,
                "stat": "quickmath_correct_answers"
            },

            # 综合成就
            "all_games_played": {
                "title": "游戏探索者",
                "description": "玩过所有类型的游戏",
                "category": "general",
                "icon": "🎮",
                "threshold": None,  # 特殊成就，需要单独检查
                "stat": None
            }
        }

    def _load_achievements(self) -> Dict[str, Dict]:
        """从文件加载成就数据"""
        if os.path.exists(self.achievements_file):
            try:
                with open(self.achievements_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass

        # 初始化成就数据
        achievements = {}
        for ach_id, ach_def in self.achievement_definitions.items():
            achievements[ach_id] = {
                "unlocked": False,
                "unlocked_at": None,
                "title": ach_def["title"],
                "description": ach_def["description"],
                "category": ach_def["category"],
                "icon": ach_def["icon"]
            }

        return achievements

    def _load_stats(self) -> None:
        """从成就文件加载统计数据"""
        if os.path.exists(self.achievements_file):
            try:
                with open(self.achievements_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if "stats" in data:
                        # 更新统计数据，保留新添加的统计项
                        for key, value in data["stats"].items():
                            if key in self.stats:
                                self.stats[key] = value
            except:
                pass

    def _save_data(self) -> None:
        """保存成就和统计数据到文件"""
        data = self.achievements.copy()
        data["stats"] = self.stats

        with open(self.achievements_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def update_stat(self, stat_name: str, value: int = 1, is_increment: bool = True) -> List[str]:
        """
        更新统计数据并检查是否解锁新成就

        参数:
            stat_name: 统计项名称
            value: 数值（如果是增量则为增加的值，否则为新值）
            is_increment: 是否为增量更新

        返回:
            新解锁的成就ID列表
        """
        if stat_name not in self.stats:
            return []

        # 更新统计数据
        if is_increment:
            self.stats[stat_name] += value
        else:
            # 对于高分等统计，只保留最大值
            if stat_name.endswith("_high_score"):
                self.stats[stat_name] = max(self.stats[stat_name], value)
            else:
                self.stats[stat_name] = value

        # 检查是否解锁新成就
        new_achievements = self._check_achievements()

        # 保存数据
        self._save_data()

        return new_achievements

    def _check_achievements(self) -> List[str]:
        """检查是否有新成就可以解锁"""
        new_achievements = []

        # 检查常规成就
        for ach_id, ach_def in self.achievement_definitions.items():
            # 已解锁的成就不再检查
            if self.achievements[ach_id]["unlocked"]:
                continue

            # 处理特殊成就
            if ach_id == "all_games_played":
                if (self.stats["twentyfour_games_played"] > 0 and
                        self.stats["snake_games_played"] > 0 and
                        self.stats["tetris_games_played"] > 0 and
                        self.stats["quickmath_games_played"] > 0):
                    self._unlock_achievement(ach_id)
                    new_achievements.append(ach_id)
                continue

            # 检查常规成就
            stat_name = ach_def["stat"]
            threshold = ach_def["threshold"]

            if (stat_name in self.stats and
                    self.stats[stat_name] >= threshold):
                self._unlock_achievement(ach_id)
                new_achievements.append(ach_id)

        return new_achievements

    def _unlock_achievement(self, ach_id: str) -> None:
        """解锁指定成就"""
        if ach_id in self.achievements and not self.achievements[ach_id]["unlocked"]:
            self.achievements[ach_id]["unlocked"] = True
            self.achievements[ach_id]["unlocked_at"] = datetime.now().isoformat()

    def get_unlocked_achievements(self, category: Optional[str] = None) -> List[Dict]:
        """
        获取已解锁的成就

        参数:
            category: 可选，指定类别，如"calculator"、"snake"等

        返回:
            已解锁成就的列表
        """
        unlocked = []
        for ach in self.achievements.values():
            if ach["unlocked"] and (category is None or ach["category"] == category):
                unlocked.append(ach)

        # 按解锁时间排序
        return sorted(unlocked, key=lambda x: x["unlocked_at"], reverse=True)

    def get_locked_achievements(self, category: Optional[str] = None) -> List[Dict]:
        """
        获取未解锁的成就

        参数:
            category: 可选，指定类别

        返回:
            未解锁成就的列表
        """
        locked = []
        for ach_id, ach in self.achievements.items():
            if not ach["unlocked"] and (category is None or ach["category"] == category):
                # 添加进度信息
                progress = 0
                total = 0

                if ach_id in self.achievement_definitions:
                    def_data = self.achievement_definitions[ach_id]
                    if def_data["stat"] and def_data["threshold"]:
                        total = def_data["threshold"]
                        progress = min(self.stats.get(def_data["stat"], 0), total)

                locked.append({
                    **ach,
                    "progress": progress,
                    "total": total
                })

        return locked

    def get_achievement_progress(self, ach_id: str) -> Tuple[int, int]:
        """
        获取指定成就的进度

        返回:
            (当前进度, 目标进度)
        """
        if ach_id not in self.achievement_definitions:
            return (0, 0)

        def_data = self.achievement_definitions[ach_id]

        if not def_data["stat"] or not def_data["threshold"]:
            return (0, 0)

        current = self.stats.get(def_data["stat"], 0)
        target = def_data["threshold"]

        return (min(current, target), target)

    def get_category_stats(self, category: str) -> Dict:
        """获取指定类别的统计数据"""
        # 找出该类别下的所有成就
        category_achievements = [
            ach_id for ach_id, ach_def in self.achievement_definitions.items()
            if ach_def["category"] == category
        ]

        # 计算已解锁比例
        unlocked_count = sum(
            1 for ach_id in category_achievements
            if self.achievements[ach_id]["unlocked"]
        )
        total_count = len(category_achievements)
        completion_rate = (unlocked_count / total_count) * 100 if total_count > 0 else 0

        return {
            "unlocked_count": unlocked_count,
            "total_count": total_count,
            "completion_rate": completion_rate,
            "stats": {k: v for k, v in self.stats.items() if k.startswith(category)}
        }
