import mujoco
import numpy as np
from pathlib import Path

# 1. 加载官方人形模型

script_dir = Path(__file__).resolve().parent
model_path = (script_dir.parent.parent.parent / 'mujoco' / 'model' / 'humanoid' / 'humanoid.xml').resolve()

model = mujoco.MjModel.from_xml_path(str(model_path))
data = mujoco.MjData(model)

# --------------------------
# 核心：正运动学函数（可直接复用）
# 输入：关节角度qpos，输出：手部末端坐标x,y,z
# --------------------------
def forward_kinematics(qpos):
    # 设置关节角度
    data.qpos[:] = qpos
    # MuJoCo内置正运动学求解（自动计算所有身体位置）
    mujoco.mj_forward(model, data)
    # 获取左手末端坐标（"left_hand"是人形模型内置手部body名称）
    print("body names: <<", data.body)
    hand_pos = data.body("left_hand").xpos.copy()
    return hand_pos

# --------------------------
# 测试：控制手臂关节，计算手部位置
# --------------------------
if __name__ == "__main__":
    # 初始化全部关节为0（自然站立）
    qpos_init = np.zeros(model.nq)
    # 控制左肩、手肘关节角度，让手臂抬起
    qpos_init[7] = 0.5   # 左肩旋转角度（弧度）
    qpos_init[9] = -0.8  # 左肘弯曲角度（弧度）

    # 调用正运动学，计算手部位置
    hand_xyz = forward_kinematics(qpos_init)
    print(f"手部末端坐标：x={hand_xyz[0]:.3f}, y={hand_xyz[1]:.3f}, z={hand_xyz[2]:.3f}")

    # 可视化查看效果
    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            mujoco.mj_step(model, data)
            viewer.sync()