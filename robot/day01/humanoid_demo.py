
import mujoco
from mujoco import viewer
from pathlib import Path

# 1. 加载本地 humanoid 模型文件（使用 ASCII 路径避免 Windows 路径编码问题）
# D:\works\mujoco\model\humanoid\humanoid.xml
model_path = Path('d:/works/mujoco/model/humanoid/humanoid.xml')
model = mujoco.MjModel.from_xml_path(str(model_path))
data = mujoco.MjData(model)

# 2. 启动可视化仿真窗口，运行100秒
with mujoco.viewer.launch_passive(model, data) as viewer:
    # 开启自由相机模式，鼠标可拖拽旋转、缩放视角
    viewer.cam.type = mujoco.mjtCamera.mjCAMERA_FREE
    while viewer.is_running() and data.time < 1000*200:
        # 执行物理仿真一步
        mujoco.mj_step(model, data)
        # 同步可视化画面
        viewer.sync()
