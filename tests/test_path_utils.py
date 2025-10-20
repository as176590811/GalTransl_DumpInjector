"""
测试路径工具函数
"""

import unittest
import os
import sys
import tempfile

# 添加src目录到路径以便导入
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# 创建一个简单的测试类来访问静态方法
class PathTester:
    @staticmethod
    def is_subdirectory(child_path: str, parent_path: str) -> bool:
        """
        判断child_path是否是parent_path的子目录
        """
        try:
            # 规范化路径
            child_path = os.path.normpath(child_path)
            parent_path = os.path.normpath(parent_path)
            
            # 获取相对路径
            rel_path = os.path.relpath(child_path, parent_path)
            
            # 如果相对路径不以..开头，则child_path是parent_path的子目录
            return not rel_path.startswith('..')
        except ValueError:
            # 在某些情况下（如不同驱动器），relpath可能抛出ValueError
            return False


class TestPathUtils(unittest.TestCase):
    """测试路径工具函数"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录结构用于测试
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_root = self.test_dir.name
        
        # 创建测试目录结构
        self.game_dir = os.path.join(self.test_root, "game")
        self.script_dir = os.path.join(self.game_dir, "script")
        self.other_dir = os.path.join(self.test_root, "other")
        
        os.makedirs(self.script_dir, exist_ok=True)
        os.makedirs(self.other_dir, exist_ok=True)
    
    def tearDown(self):
        """测试后清理"""
        self.test_dir.cleanup()
    
    def test_is_subdirectory_positive(self):
        """测试子目录情况"""
        # 测试script是game的子目录
        self.assertTrue(PathTester.is_subdirectory(
            self.script_dir, 
            self.game_dir
        ))
        
        # 测试相同目录情况
        self.assertTrue(PathTester.is_subdirectory(
            self.game_dir, 
            self.game_dir
        ))
    
    def test_is_subdirectory_negative(self):
        """测试非子目录情况"""
        # 测试other不是game的子目录
        self.assertFalse(PathTester.is_subdirectory(
            self.other_dir, 
            self.game_dir
        ))
        
        # 测试game不是script的子目录
        self.assertFalse(PathTester.is_subdirectory(
            self.game_dir, 
            self.script_dir
        ))


if __name__ == '__main__':
    unittest.main()