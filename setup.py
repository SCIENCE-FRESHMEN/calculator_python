import os
import sys
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.building.api import COLLECT, EXE, PYZ
from PyInstaller.building.build_main import Analysis


def build():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 分析主程序
    a = Analysis(
        ['main.py'],
        pathex=[current_dir],
        binaries=[],
        datas=collect_data_files('PyQt5'),
        hiddenimports=[],
        hookspath=[],
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=None,
        noarchive=False
    )

    # 创建PYZ文件
    pyz = PYZ(a.pure, a.zipped_data, cipher=None)

    # 创建可执行文件
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='儿童益智计算器',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,  # 不显示控制台窗口
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=os.path.join(current_dir, 'resources', 'images', 'calculator.ico')  # 图标文件
    )

    # 收集所有文件
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='儿童益智计算器'
    )

    return coll


if __name__ == '__main__':
    build()
