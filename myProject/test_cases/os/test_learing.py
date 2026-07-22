"""
test_learing.py - 简单的 pytest 测试用例示例
"""

import os
import pytest


class TestSimple:
    """简单的 pytest 测试类示例"""

    def test_addition(self):
        """测试加法"""
        assert 1 + 1 == 2

    def test_subtraction(self):
        """测试减法"""
        assert 3 - 1 == 2

    def test_string_upper(self):
        """测试字符串大写"""
        assert "hello".upper() == "HELLO"

    def test_list_contains(self):
        """测试列表包含"""
        assert 3 in [1, 2, 3, 4]


class TestFileOperations:
    """测试文件路径相关的操作"""

    def test_file_exists(self):
        """测试当前文件是否存在"""
        assert os.path.isfile(__file__)

    def test_path_join(self):
        """测试路径拼接"""
        path = os.path.join("a", "b", "c.txt")
        assert path == "a\\b\\c.txt" or path == "a/b/c.txt"

    def test_path_basename(self):
        """测试获取文件名"""
        assert os.path.basename(__file__) == "test_learing.py"

    def test_path_dirname(self):
        """测试获取目录名"""
        dirname = os.path.dirname(__file__)
        assert dirname.endswith("os")


class TestEnviron:
    """测试环境变量相关操作"""

    def test_temp_env_exists(self):
        """测试临时环境变量"""
        assert "TEMP" in os.environ or "TMP" in os.environ

    def test_set_and_delete_env(self):
        """测试设置和删除环境变量"""
        os.environ["TEST_VAR"] = "hello"
        assert os.environ.get("TEST_VAR") == "hello"
        del os.environ["TEST_VAR"]
        assert "TEST_VAR" not in os.environ


class TestDivisionByZero:
    """测试异常处理"""

    def test_zero_division(self):
        """测试除以零抛出异常"""
        with pytest.raises(ZeroDivisionError):
            result = 1 / 0

    def test_type_error(self):
        """测试类型错误抛出异常"""
        with pytest.raises(TypeError):
            result = "1" + 1

    def test_file_not_found(self):
        """测试文件不存在抛出异常"""
        with pytest.raises(FileNotFoundError):
            with open("non_existent_file_xyz.txt"):
                pass


@pytest.fixture
def sample_list():
    """pytest fixture，返回一个示例列表"""
    return [1, 2, 3, 4, 5]


class TestWithFixture:
    """测试使用 fixture"""

    def test_list_sum(self, sample_list):
        """测试列表求和"""
        assert sum(sample_list) == 15

    def test_list_length(self, sample_list):
        """测试列表长度"""
        assert len(sample_list) == 5

    def test_list_max(self, sample_list):
        """测试列表最大值"""
        assert max(sample_list) == 5

    def test_list_min(self, sample_list):
        """测试列表最小值"""
        assert min(sample_list) == 1


@pytest.mark.parametrize("input_val,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
    (5, 25),
])
def test_square(input_val, expected):
    """参数化测试：计算平方"""
    assert input_val * input_val == expected


@pytest.mark.skip(reason="此测试被标记跳过，仅作演示")
def test_skipped():
    """演示跳过的测试"""
    assert False


class TestOsPathOperations:
    """测试 os.path 各种操作"""

    @pytest.mark.parametrize("path,expected_stem", [
        ("file.txt", "file"),
        ("/path/to/archive.tar.gz", "archive.tar"),
        ("data.csv", "data"),
    ])
    def test_splitext(self, path, expected_stem):
        """测试 os.path.splitext"""
        stem, ext = os.path.splitext(path)
        assert stem == expected_stem

    def test_abspath(self):
        """测试 os.path.abspath"""
        abs_path = os.path.abspath("test.txt")
        assert os.path.isabs(abs_path)
        assert abs_path.endswith("test.txt")

    def test_exists_return_type(self):
        """测试 os.path.exists 返回类型"""
        result = os.path.exists(__file__)
        assert isinstance(result, bool)
        assert result is True
