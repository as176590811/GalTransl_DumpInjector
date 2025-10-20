"""
手动测试所有标签页的路径更新功能
"""

import sys
import os

# 添加src目录到路径以便导入
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# 创建一个简单的测试来验证路径更新逻辑
class MockFileSelector:
    def __init__(self, initial_path=""):
        self.path = initial_path
    
    def get_path(self):
        return self.path
    
    def set_path(self, path):
        self.path = path
        print(f"  设置路径为: {path}")

class TestMsgToolTab:
    def __init__(self):
        self.json_jp_selector = MockFileSelector()
        self.json_cn_selector = MockFileSelector()
        self.script_cn_selector = MockFileSelector()
    
    def _is_subdirectory(self, child_path: str, parent_path: str) -> bool:
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
    
    def _on_script_jp_path_changed(self, path: str):
        """当日文脚本文件夹路径变化时，自动更新相关文件夹路径"""
        print(f"msg-tool标签页 - 日文脚本文件夹路径变化: {path}")
        if not path:
            return
            
        # 获取日文脚本文件夹的父目录
        jp_script_parent = os.path.dirname(path)
        print(f"  父目录: {jp_script_parent}")
        
        # 更新日文JSON保存文件夹
        json_jp_folder = self.json_jp_selector.get_path()
        print(f"  当前日文JSON保存文件夹: {json_jp_folder}")
        if not json_jp_folder or not self._is_subdirectory(json_jp_folder, path):
            # 不是子目录，更新为父目录下的gt_input文件夹
            new_json_jp_folder = os.path.join(jp_script_parent, "gt_input")
            print(f"  更新日文JSON保存文件夹为: {new_json_jp_folder}")
            self.json_jp_selector.set_path(new_json_jp_folder)
        else:
            print("  日文JSON保存文件夹已是子目录，无需更新")
        
        # 更新译文JSON文件夹
        json_cn_folder = self.json_cn_selector.get_path()
        print(f"  当前译文JSON文件夹: {json_cn_folder}")
        if not json_cn_folder or not self._is_subdirectory(json_cn_folder, path):
            # 不是子目录，更新为父目录的父目录下的gt_output文件夹
            parent_of_parent = os.path.dirname(jp_script_parent)
            new_json_cn_folder = os.path.join(parent_of_parent, "gt_output")
            print(f"  更新译文JSON文件夹为: {new_json_cn_folder}")
            self.json_cn_selector.set_path(new_json_cn_folder)
        else:
            print("  译文JSON文件夹已是子目录，无需更新")
        
        # 更新译文脚本保存文件夹
        script_cn_folder = self.script_cn_selector.get_path()
        print(f"  当前译文脚本保存文件夹: {script_cn_folder}")
        if not script_cn_folder or not self._is_subdirectory(script_cn_folder, path):
            # 不是子目录，更新为父目录的父目录下的script_output文件夹
            parent_of_parent = os.path.dirname(jp_script_parent)
            new_script_cn_folder = os.path.join(parent_of_parent, "script_output")
            print(f"  更新译文脚本保存文件夹为: {new_script_cn_folder}")
            self.script_cn_selector.set_path(new_script_cn_folder)
        else:
            print("  译文脚本保存文件夹已是子目录，无需更新")

class TestRegexTab:
    def __init__(self):
        self.json_jp_selector = MockFileSelector()
        self.json_cn_selector = MockFileSelector()
        self.script_cn_selector = MockFileSelector()
    
    def _is_subdirectory(self, child_path: str, parent_path: str) -> bool:
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
    
    def _on_script_jp_path_changed(self, path: str):
        """当日文脚本文件夹路径变化时，自动更新相关文件夹路径"""
        print(f"正则表达式标签页 - 日文脚本文件夹路径变化: {path}")
        if not path:
            return
            
        # 获取日文脚本文件夹的父目录
        jp_script_parent = os.path.dirname(path)
        print(f"  父目录: {jp_script_parent}")
        
        # 更新日文JSON保存文件夹
        json_jp_folder = self.json_jp_selector.get_path()
        print(f"  当前日文JSON保存文件夹: {json_jp_folder}")
        if not json_jp_folder or not self._is_subdirectory(json_jp_folder, path):
            # 不是子目录，更新为父目录下的gt_input文件夹
            new_json_jp_folder = os.path.join(jp_script_parent, "gt_input")
            print(f"  更新日文JSON保存文件夹为: {new_json_jp_folder}")
            self.json_jp_selector.set_path(new_json_jp_folder)
        else:
            print("  日文JSON保存文件夹已是子目录，无需更新")
        
        # 更新译文JSON文件夹
        json_cn_folder = self.json_cn_selector.get_path()
        print(f"  当前译文JSON文件夹: {json_cn_folder}")
        if not json_cn_folder or not self._is_subdirectory(json_cn_folder, path):
            # 不是子目录，更新为父目录的父目录下的gt_output文件夹
            parent_of_parent = os.path.dirname(jp_script_parent)
            new_json_cn_folder = os.path.join(parent_of_parent, "gt_output")
            print(f"  更新译文JSON文件夹为: {new_json_cn_folder}")
            self.json_cn_selector.set_path(new_json_cn_folder)
        else:
            print("  译文JSON文件夹已是子目录，无需更新")
        
        # 更新译文脚本保存文件夹
        script_cn_folder = self.script_cn_selector.get_path()
        print(f"  当前译文脚本保存文件夹: {script_cn_folder}")
        if not script_cn_folder or not self._is_subdirectory(script_cn_folder, path):
            # 不是子目录，更新为父目录的父目录下的script_output文件夹
            parent_of_parent = os.path.dirname(jp_script_parent)
            new_script_cn_folder = os.path.join(parent_of_parent, "script_output")
            print(f"  更新译文脚本保存文件夹为: {new_script_cn_folder}")
            self.script_cn_selector.set_path(new_script_cn_folder)
        else:
            print("  译文脚本保存文件夹已是子目录，无需更新")

def test_case_1():
    """测试用例1: 所有路径都不是子目录"""
    print("=== 测试用例1: 所有路径都不是子目录 ===")
    
    # 测试msg-tool标签页
    print("--- msg-tool标签页 ---")
    msg_tool_tab = TestMsgToolTab()
    jp_script_path = r"E:\game\script"
    msg_tool_tab._on_script_jp_path_changed(jp_script_path)
    
    # 测试正则表达式标签页
    print("\n--- 正则表达式标签页 ---")
    regex_tab = TestRegexTab()
    regex_tab._on_script_jp_path_changed(jp_script_path)
    print()

def test_case_2():
    """测试用例2: 部分路径是子目录"""
    print("=== 测试用例2: 部分路径是子目录 ===")
    
    # 测试msg-tool标签页
    print("--- msg-tool标签页 ---")
    msg_tool_tab = TestMsgToolTab()
    # 设置已经是子目录的路径
    msg_tool_tab.json_jp_selector.set_path(r"E:\game\script\json_jp")
    msg_tool_tab.json_cn_selector.set_path(r"E:\game\json_cn")
    jp_script_path = r"E:\game\script"
    msg_tool_tab._on_script_jp_path_changed(jp_script_path)
    
    # 测试正则表达式标签页
    print("\n--- 正则表达式标签页 ---")
    regex_tab = TestRegexTab()
    # 设置已经是子目录的路径
    regex_tab.json_jp_selector.set_path(r"E:\game\script\json_jp")
    regex_tab.json_cn_selector.set_path(r"E:\game\json_cn")
    regex_tab._on_script_jp_path_changed(jp_script_path)
    print()

if __name__ == "__main__":
    test_case_1()
    test_case_2()