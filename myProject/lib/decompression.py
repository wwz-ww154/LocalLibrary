"""
解压模块 - 支持多种压缩格式的递归解压
支持格式: .zip, .tar, .tar.gz, .tgz, .tar.bz2, .tbz2, .tar.xz, .txz, .gz, .bz2, .xz, .rar, .7z
默认解压密码: fruit
"""

import os
import zipfile
import tarfile
import shutil
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 默认解压密码
DEFAULT_PASSWORD = "fruit"

# 支持的压缩格式及其对应的文件后缀
SUPPORTED_EXTENSIONS = {
    '.zip': 'zip',
    '.tar': 'tar',
    '.tar.gz': 'targz',
    '.tgz': 'targz',
    '.tar.bz2': 'tarbz2',
    '.tbz2': 'tarbz2',
    '.tar.xz': 'tarxz',
    '.txz': 'tarxz',
    '.gz': 'gz',
    '.bz2': 'bz2',
    '.xz': 'xz',
    '.rar': 'rar',
    '.7z': 'sevenz',
}


def extract_zip(file_path: str, extract_to: str, password: str = DEFAULT_PASSWORD) -> bool:
    """解压 .zip 文件"""
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            # 尝试无密码解压
            try:
                zf.extractall(extract_to)
                logger.info(f"成功解压 (无密码): {file_path}")
                return True
            except (RuntimeError, zipfile.BadZipFile):
                pass

            # 尝试使用密码解压
            try:
                zf.setpassword(password.encode('utf-8'))
                zf.extractall(extract_to)
                logger.info(f"成功解压 (使用密码): {file_path}")
                return True
            except (RuntimeError, zipfile.BadZipFile) as e:
                logger.error(f"解压失败 (密码错误或文件损坏): {file_path} - {e}")
                return False
    except Exception as e:
        logger.error(f"读取 zip 文件失败: {file_path} - {e}")
        return False


def extract_tar(file_path: str, extract_to: str, **kwargs) -> bool:
    """解压 .tar 文件"""
    try:
        with tarfile.open(file_path, 'r') as tf:
            tf.extractall(extract_to)
            logger.info(f"成功解压: {file_path}")
            return True
    except Exception as e:
        logger.error(f"解压 tar 文件失败: {file_path} - {e}")
        return False


def extract_targz(file_path: str, extract_to: str, **kwargs) -> bool:
    """解压 .tar.gz / .tgz 文件"""
    try:
        with tarfile.open(file_path, 'r:gz') as tf:
            tf.extractall(extract_to)
            logger.info(f"成功解压: {file_path}")
            return True
    except Exception as e:
        logger.error(f"解压 tar.gz 文件失败: {file_path} - {e}")
        return False


def extract_tarbz2(file_path: str, extract_to: str, **kwargs) -> bool:
    """解压 .tar.bz2 / .tbz2 文件"""
    try:
        with tarfile.open(file_path, 'r:bz2') as tf:
            tf.extractall(extract_to)
            logger.info(f"成功解压: {file_path}")
            return True
    except Exception as e:
        logger.error(f"解压 tar.bz2 文件失败: {file_path} - {e}")
        return False


def extract_tarxz(file_path: str, extract_to: str, **kwargs) -> bool:
    """解压 .tar.xz / .txz 文件"""
    try:
        with tarfile.open(file_path, 'r:xz') as tf:
            tf.extractall(extract_to)
            logger.info(f"成功解压: {file_path}")
            return True
    except Exception as e:
        logger.error(f"解压 tar.xz 文件失败: {file_path} - {e}")
        return False


def extract_gz(file_path: str, extract_to: str, **kwargs) -> bool:
    """解压 .gz 文件（仅解压单个文件）"""
    import gzip
    try:
        output_name = Path(file_path).stem  # 去掉 .gz 后缀
        output_path = os.path.join(extract_to, output_name)
        with gzip.open(file_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        logger.info(f"成功解压: {file_path} -> {output_path}")
        return True
    except Exception as e:
        logger.error(f"解压 gz 文件失败: {file_path} - {e}")
        return False


def extract_bz2(file_path: str, extract_to: str, **kwargs) -> bool:
    """解压 .bz2 文件（仅解压单个文件）"""
    import bz2
    try:
        output_name = Path(file_path).stem
        output_path = os.path.join(extract_to, output_name)
        with bz2.open(file_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        logger.info(f"成功解压: {file_path} -> {output_path}")
        return True
    except Exception as e:
        logger.error(f"解压 bz2 文件失败: {file_path} - {e}")
        return False


def extract_xz(file_path: str, extract_to: str, **kwargs) -> bool:
    """解压 .xz 文件（仅解压单个文件）"""
    import lzma
    try:
        output_name = Path(file_path).stem
        output_path = os.path.join(extract_to, output_name)
        with lzma.open(file_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        logger.info(f"成功解压: {file_path} -> {output_path}")
        return True
    except Exception as e:
        logger.error(f"解压 xz 文件失败: {file_path} - {e}")
        return False


def extract_rar(file_path: str, extract_to: str, password: str = DEFAULT_PASSWORD) -> bool:
    """解压 .rar 文件（需要安装 rarfile 库和 UnRAR 工具）"""
    try:
        import rarfile
    except ImportError:
        logger.warning("rarfile 库未安装，尝试使用 patool 或命令行工具...")
        return _extract_rar_fallback(file_path, extract_to, password)

    try:
        with rarfile.RarFile(file_path) as rf:
            # 尝试无密码
            try:
                rf.extractall(extract_to)
                logger.info(f"成功解压 (无密码): {file_path}")
                return True
            except (rarfile.RarWrongPassword, rarfile.RarCannotExec):
                pass

            # 尝试使用密码
            try:
                rf.setpassword(password)
                rf.extractall(extract_to)
                logger.info(f"成功解压 (使用密码): {file_path}")
                return True
            except (rarfile.RarWrongPassword, rarfile.RarCannotExec) as e:
                logger.error(f"解压 rar 文件失败: {file_path} - {e}")
                return False
    except Exception as e:
        logger.error(f"读取 rar 文件失败: {file_path} - {e}")
        return False


def _extract_rar_fallback(file_path: str, extract_to: str, password: str = DEFAULT_PASSWORD) -> bool:
    """使用 patool 或命令行工具作为 rarfile 的备用方案"""
    try:
        import patoolib
        patoolib.extract_archive(file_path, outdir=extract_to, password=password)
        logger.info(f"成功解压 (通过 patool): {file_path}")
        return True
    except ImportError:
        pass
    except Exception as e:
        logger.warning(f"patool 解压失败: {file_path} - {e}")

    # 尝试使用命令行 unrar
    try:
        import subprocess
        result = subprocess.run(
            ['unrar', 'x', f'-p{password}', '-y', file_path, extract_to],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            logger.info(f"成功解压 (通过 unrar 命令): {file_path}")
            return True
        else:
            logger.error(f"unrar 命令失败: {file_path} - {result.stderr}")
            return False
    except FileNotFoundError:
        logger.error("系统中未安装 unrar 工具，无法解压 .rar 文件")
        return False
    except Exception as e:
        logger.error(f"unrar 命令执行异常: {file_path} - {e}")
        return False


def extract_sevenz(file_path: str, extract_to: str, password: str = DEFAULT_PASSWORD) -> bool:
    """解压 .7z 文件（需要安装 py7zr 库或 7z 命令行工具）"""
    try:
        import py7zr
    except ImportError:
        logger.warning("py7zr 库未安装，尝试使用命令行工具...")
        return _extract_sevenz_fallback(file_path, extract_to, password)

    try:
        with py7zr.SevenZipFile(file_path, mode='r', password=password) as sz:
            sz.extractall(path=extract_to)
            logger.info(f"成功解压: {file_path}")
            return True
    except Exception as e:
        logger.error(f"解压 7z 文件失败: {file_path} - {e}")
        return False


def _extract_sevenz_fallback(file_path: str, extract_to: str, password: str = DEFAULT_PASSWORD) -> bool:
    """使用 7z 命令行工具作为备用方案"""
    try:
        import subprocess
        result = subprocess.run(
            ['7z', 'x', f'-p{password}', '-y', f'-o{extract_to}', file_path],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            logger.info(f"成功解压 (通过 7z 命令): {file_path}")
            return True
        else:
            logger.error(f"7z 命令失败: {file_path} - {result.stderr}")
            return False
    except FileNotFoundError:
        logger.error("系统中未安装 7z 工具，无法解压 .7z 文件")
        return False
    except Exception as e:
        logger.error(f"7z 命令执行异常: {file_path} - {e}")
        return False


# 映射后缀到对应的解压函数
EXTRACTORS = {
    'zip': extract_zip,
    'tar': extract_tar,
    'targz': extract_targz,
    'tarbz2': extract_tarbz2,
    'tarxz': extract_tarxz,
    'gz': extract_gz,
    'bz2': extract_bz2,
    'xz': extract_xz,
    'rar': extract_rar,
    'sevenz': extract_sevenz,
}


def get_archive_type(file_path: str) -> str | None:
    """
    根据文件路径判断压缩包类型
    返回类型键值，若不支持则返回 None
    """
    file_path_lower = file_path.lower()
    # 按后缀长度降序匹配，优先匹配长后缀（如 .tar.gz）
    sorted_exts = sorted(SUPPORTED_EXTENSIONS.items(), key=lambda x: -len(x[0]))
    for ext, archive_type in sorted_exts:
        if file_path_lower.endswith(ext):
            return archive_type
    return None


def extract_single_archive(file_path: str, extract_to: str = None, password: str = DEFAULT_PASSWORD) -> bool:
    """
    解压单个压缩文件

    Args:
        file_path: 压缩文件路径
        extract_to: 解压目标目录，默认为压缩文件同名目录（不含后缀）
        password: 解压密码

    Returns:
        解压成功返回 True，失败返回 False
    """
    if not os.path.isfile(file_path):
        logger.error(f"文件不存在: {file_path}")
        return False

    archive_type = get_archive_type(file_path)
    if archive_type is None:
        logger.warning(f"不支持的压缩格式: {file_path}")
        return False

    # 默认解压到与压缩文件同名的目录（不含后缀）
    if extract_to is None:
        extract_to = os.path.splitext(file_path)[0]
        # 对于双后缀（如 .tar.gz），去掉整个后缀
        file_path_lower = file_path.lower()
        for ext in sorted(SUPPORTED_EXTENSIONS.keys(), key=lambda x: -len(x[0])):
            if file_path_lower.endswith(ext):
                name_without_ext = file_path[:-len(ext)] if file_path_lower.endswith(ext) else file_path
                extract_to = name_without_ext
                break

    # 确保目标目录存在
    os.makedirs(extract_to, exist_ok=True)

    extractor = EXTRACTORS.get(archive_type)
    if extractor is None:
        logger.error(f"未找到 {archive_type} 对应的解压函数")
        return False

    logger.info(f"开始解压: {file_path} -> {extract_to}")
    return extractor(file_path, extract_to, password=password)


def extract_all_in_directory(directory: str, password: str = DEFAULT_PASSWORD, remove_archive: bool = False) -> int:
    """
    递归解压目录下所有支持的压缩文件

    Args:
        directory: 目标目录路径
        password: 解压密码
        remove_archive: 解压后是否删除原压缩文件

    Returns:
        成功解压的文件数量
    """
    if not os.path.isdir(directory):
        logger.error(f"目录不存在: {directory}")
        return 0

    success_count = 0
    fail_count = 0

    # 使用 os.walk 递归遍历目录
    for root, dirs, files in os.walk(directory):
        for filename in sorted(files):
            file_path = os.path.join(root, filename)

            # 跳过非压缩文件
            archive_type = get_archive_type(file_path)
            if archive_type is None:
                continue

            # 解压到当前目录
            extract_to = root
            logger.info(f"发现压缩文件: {file_path}")

            # 为了避免重名冲突，建议解压到单独的子目录
            # 但如果压缩包内包含顶层目录，也可以直接解压到当前目录
            # 这里选择解压到以压缩文件名命名的子目录
            file_stem = filename
            for ext in sorted(SUPPORTED_EXTENSIONS.keys(), key=lambda x: -len(x[0])):
                if filename.lower().endswith(ext):
                    file_stem = filename[:-len(ext)]
                    break
            extract_to = os.path.join(root, file_stem)

            if extract_single_archive(file_path, extract_to=extract_to, password=password):
                success_count += 1
                if remove_archive:
                    try:
                        os.remove(file_path)
                        logger.info(f"已删除原压缩文件: {file_path}")
                    except OSError as e:
                        logger.error(f"删除文件失败: {file_path} - {e}")

                # 递归解压：解压完成后，扫描解压目录中是否还有压缩文件
                nested_count = extract_all_in_directory(extract_to, password=password, remove_archive=remove_archive)
                success_count += nested_count
            else:
                fail_count += 1

    if success_count > 0 or fail_count > 0:
        logger.info(f"目录解压完成: {directory} | 成功: {success_count}, 失败: {fail_count}")

    return success_count


def decompress_entry(path: str, password: str = DEFAULT_PASSWORD, recursive: bool = True,
                     remove_archive: bool = False) -> int:
    """
    主入口函数 - 解压文件或目录

    Args:
        path: 文件或目录路径
        password: 解压密码
        recursive: 是否递归解压子目录中的压缩文件
        remove_archive: 解压后是否删除原压缩文件

    Returns:
        成功解压的文件数量
    """
    if not os.path.exists(path):
        logger.error(f"路径不存在: {path}")
        return 0

    if os.path.isfile(path):
        # 解压单个文件
        if extract_single_archive(path, password=password):
            return 1
        return 0
    elif os.path.isdir(path):
        # 解压目录
        if recursive:
            return extract_all_in_directory(path, password=password, remove_archive=remove_archive)
        else:
            # 仅解压当前目录，不递归子目录
            success_count = 0
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    if extract_single_archive(item_path, password=password):
                        success_count += 1
            return success_count
    else:
        logger.error(f"未知路径类型: {path}")
        return 0


# 简单的命令行入口
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("用法: python decompression.py <路径> [密码]")
        print("示例: python decompression.py ./archives fruit")
        sys.exit(1)

    target_path = sys.argv[1]
    pwd = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PASSWORD

    count = decompress_entry(target_path, password=pwd, recursive=True)
    print(f"解压完成，共成功解压 {count} 个文件")
