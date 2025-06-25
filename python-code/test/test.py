import os
from pymol import cmd, finish_launching
from pymol import util

# 强制设置虚拟显示
os.environ["DISPLAY"] = ":99"

# 初始化 PyMOL（控制台模式 + 日志）
finish_launching(['pymol', '-c', '-k'])


try:
    # 加载文件并指定对象名
    cmd.load("../4K3A.pdb", "my_protein", format="pdb", quiet=0)

    # 检查对象列表
    objects = cmd.get_names()
    if "my_protein" not in objects:
        print("加载失败：对象未创建！")
        exit(1)

    print("文件加载成功")
    # 配置显示
    cmd.hide("everything")
    cmd.show("cartoon")
    cmd.color("green")
    cmd.orient()
    cmd.zoom("all", 5)
    print(dir(util))
    try:
        # 尝试导出 WebGL（需 PyMOL ≥ 2.5.0）
        cmd.util.export_html("output.html", format="webgl")
    except AttributeError:
        # 回退到 PNG 导出
        cmd.png("fallback.png", width=800, height=600)
        print("WebGL 不可用，已生成 PNG 图片")

except Exception as e:
    print(f"PyMOL 操作失败：{str(e)}")
finally:
    cmd.quit()