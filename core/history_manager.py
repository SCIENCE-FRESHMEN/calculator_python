import json
import os
from datetime import datetime
from typing import List, Dict


class HistoryManager:
    """管理计算历史记录的持久化存储和读取"""

    def __init__(self, data_dir: str = "data", filename: str = "history.json"):
        """初始化历史记录管理器"""
        self.data_dir = data_dir
        self.filename = filename
        self.file_path = os.path.join(data_dir, filename)

        # 确保数据目录存在
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # 加载现有历史记录
        self.history = self._load_history()

    def _load_history(self) -> List[Dict]:
        """从文件加载历史记录"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # 如果文件损坏或无法读取，返回空列表
                return []
        return []

    def _save_history(self) -> None:
        """将历史记录保存到文件"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"保存历史记录失败: {e}")

    def add_entry(self, expression: str, result: str, timestamp: datetime) -> None:
        """
        添加新的计算记录

        参数:
            expression: 计算表达式
            result: 计算结果
            timestamp: 时间戳
        """
        entry = {
            "expression": expression,
            "result": result,
            "timestamp": timestamp.isoformat()
        }

        # 添加到历史记录列表
        self.history.append(entry)

        # 限制历史记录数量，只保留最近的100条
        if len(self.history) > 100:
            self.history = self.history[-100:]

        # 保存到文件
        self._save_history()

    def get_history(self) -> List[Dict]:
        """获取所有历史记录"""
        return self.history.copy()

    def clear_history(self) -> None:
        """清除所有历史记录"""
        self.history = []
        self._save_history()

    def delete_entry(self, index: int) -> bool:
        """
        删除指定索引的历史记录

        参数:
            index: 要删除的记录索引

        返回:
            是否删除成功
        """
        if 0 <= index < len(self.history):
            del self.history[index]
            self._save_history()
            return True
        return False
