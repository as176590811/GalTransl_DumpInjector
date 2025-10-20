"""
测试VNTextTab路径自动更新功能
"""

import unittest
import os
import sys
import tempfile
from unittest.mock import Mock, patch

# 添加src目录到路径以便导入
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# 修复导入路径，使用相对导入
from src.gui.vntext_tab import VNTextTab
from src.models.config import Config


class TestVNTextPathUpdate(unittest.TestCase):
    """测试VNTextTab路径自动更新功能"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录结构用于测试
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_root = self.test_dir.name
        
        # 创建测试目录结构
        self.jp_script_dir = os.path.join(self.test_root, "game", "script")
        self.parent_dir = os.path.join(self.test_root, "game")
        self.grandparent_dir = self.test_root
        
        os.makedirs(self.jp_script_dir, exist_ok=True)
        os.makedirs(self.parent_dir, exist_ok=True)
        os.makedirs(self.grandparent_dir, exist_ok=True)
        
        # 创建模拟的父组件和配置
        self.mock_parent = Mock()
        self.mock_config = Mock(spec=Config)
        
        # 设置配置的默认返回值
        self.mock_config.script_jp_folder = ""
        self.mock_config.json_jp_folder = ""
        self.mock_config.json_cn_folder = ""
        self.mock_config.script_cn_folder = ""
        self.mock_config.gbk_encoding = False
        self.mock_config.sjis_replacement = False
        
    def tearDown(self):
        """测试后清理"""
        self.test_dir.cleanup()
    
    def test_is_subdirectory(self):
        """测试_is_subdirectory方法"""
        # 创建VNTextTab实例
        vntext_tab = VNTextTab(self.mock_parent, self.mock_config)
        
        # 测试子目录情况
        self.assertTrue(vntext_tab._is_subdirectory(
            os.path.join(self.test_root, "game", "script"),
            os.path.join(self.test_root, "game")
        ))
        
        # 测试非子目录情况
        self.assertFalse(vntext_tab._is_subdirectory(
            os.path.join(self.test_root, "other", "folder"),
            os.path.join(self.test_root, "game")
        ))
        
        # 测试相同目录情况
        self.assertTrue(vntext_tab._is_subdirectory(
            os.path.join(self.test_root, "game"),
            os.path.join(self.test_root, "game")
        ))
    
    @patch('tkinter.filedialog.askdirectory')
    def test_on_script_jp_path_changed_updates_paths(self, mock_askdir):
        """测试当日文脚本路径改变时是否正确更新其他路径"""
        # 创建VNTextTab实例
        vntext_tab = VNTextTab(self.mock_parent, self.mock_config)
        
        # 模拟选择日文脚本文件夹
        jp_script_path = self.jp_script_dir
        vntext_tab._on_script_jp_path_changed(jp_script_path)
        
        # 检查日文JSON保存文件夹是否更新为父目录下的gt_input
        expected_json_jp = os.path.join(self.parent_dir, "gt_input")
        actual_json_jp = vntext_tab.json_jp_selector.get_path()
        self.assertEqual(actual_json_jp, expected_json_jp)
        
        # 检查译文JSON文件夹是否更新为父目录的父目录下的gt_output
        expected_json_cn = os.path.join(self.grandparent_dir, "gt_output")
        actual_json_cn = vntext_tab.json_cn_selector.get_path()
        self.assertEqual(actual_json_cn, expected_json_cn)
        
        # 检查译文脚本保存文件夹是否更新为父目录的父目录下的script_output
        expected_script_cn = os.path.join(self.grandparent_dir, "script_output")
        actual_script_cn = vntext_tab.script_cn_selector.get_path()
        self.assertEqual(actual_script_cn, expected_script_cn)
    
    @patch('tkinter.filedialog.askdirectory')
    def test_on_script_jp_path_changed_preserves_subdirectory_paths(self, mock_askdir):
        """测试当日文脚本路径改变时，已经是子目录的路径不会被更改"""
        # 创建VNTextTab实例
        vntext_tab = VNTextTab(self.mock_parent, self.mock_config)
        
        # 设置已经是子目录的路径
        sub_json_jp = os.path.join(self.jp_script_dir, "json_jp")
        sub_json_cn = os.path.join(self.jp_script_dir, "json_cn")
        sub_script_cn = os.path.join(self.jp_script_dir, "script_cn")
        
        vntext_tab.json_jp_selector.set_path(sub_json_jp)
        vntext_tab.json_cn_selector.set_path(sub_json_cn)
        vntext_tab.script_cn_selector.set_path(sub_script_cn)
        
        # 触发路径变化
        vntext_tab._on_script_jp_path_changed(self.jp_script_dir)
        
        # 检查路径没有被更改
        self.assertEqual(vntext_tab.json_jp_selector.get_path(), sub_json_jp)
        self.assertEqual(vntext_tab.json_cn_selector.get_path(), sub_json_cn)
        self.assertEqual(vntext_tab.script_cn_selector.get_path(), sub_script_cn)


if __name__ == '__main__':
    unittest.main()