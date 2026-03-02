import os
import sys
import ctypes
import subprocess
import webbrowser

# 自动安装依赖库 psutil
try:
    import psutil
except ImportError:
    print("正在安装必要的依赖库 psutil...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil

def is_admin():
    """检查管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_disk_list():
    """获取本地硬盘分区"""
    partitions = psutil.disk_partitions()
    disks = []
    for p in partitions:
        if 'fixed' in p.opts:
            disks.append(p.mountpoint)
    return disks

def add_to_exclusion(target_path):
    """调用 PowerShell 添加排除项"""
    cmd = f"Add-MpPreference -ExclusionPath '{target_path}'"
    try:
        subprocess.run(["powershell", "-Command", cmd], check=True, capture_output=True)
        return True
    except:
        return False

def main_logic():
    # 你的 GitHub 信息
    github_username = "William-Gao2010"
    github_url = f"https://github.com/{github_username}"

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*50)
        print("      Windows Defender 磁盘一键白名单工具")
        print(f"      作者 GitHub: {github_url}")
        print("="*50)
        
        disks = get_disk_list()
        if not disks:
            print("❌ 未检测到有效磁盘。")
            break

        print("\n[当前磁盘列表]:")
        for i, disk in enumerate(disks):
            try:
                usage = psutil.disk_usage(disk)
                total_gb = usage.total // (1024**3)
                print(f"  [{i}] 磁盘 {disk}  (总容量: {total_gb} GB)")
            except:
                print(f"  [{i}] 磁盘 {disk}  (访问受限)")

        github_idx = len(disks)
        exit_idx = len(disks) + 1
        
        print("-" * 50)
        print(f"  [{github_idx}] 🚀 访问作者 GitHub 首页")
        print(f"  [{exit_idx}] ❌ 退出程序")
        print("-" * 50)

        choice = input("\n请输入编号并按回车: ").strip()
        
        if choice == str(exit_idx):
            break
        elif choice == str(github_idx):
            print(f"正在访问 {github_url} ...")
            webbrowser.open(github_url)
            input("\n回车返回菜单...")
        elif choice.isdigit() and 0 <= int(choice) < len(disks):
            target = disks[int(choice)]
            print(f"\n正在处理 {target} ...")
            if add_to_exclusion(target):
                print(f"✅ 成功！Defender 已排除 {target}")
            else:
                print(f"❌ 失败！请确保手动关闭了'篡改保护'。")
            input("\n按回车键返回...")
        else:
            print("⚠️ 输入无效。")
            os.system('pause')

if __name__ == "__main__":
    if is_admin():
        main_logic()
    else:
        # 申请管理员权限
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)