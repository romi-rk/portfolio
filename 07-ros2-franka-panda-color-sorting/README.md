# Franka Panda Color Sorting Robot

This is a little ROS 2 project I built to learn how robotic arms, computer vision, and motion planning fit together. The idea is simple: a Franka Emika Panda arm sits in front of a camera, a Python script figures out which objects are red, green, or blue, and then the arm picks each one up and drops it in the matching bin. Everything runs in Gazebo simulation, so you don't need an actual robot to try it.

I put this together mostly to teach myself ROS 2, MoveIt 2, and OpenCV at the same time, so don't expect production-grade code, just a working project I learned a lot from.

## What it actually does

- Detects red, green, and blue objects with OpenCV
- Plans and executes pick-and-place motions with MoveIt 2
- Simulates the whole thing in Gazebo, with RViz to watch the planning
- You can switch which color it's sorting without restarting anything

## What I learned building this

- How to structure a ROS 2 workspace with multiple packages
- Hooking up a vision node to a motion planning pipeline
- Using MoveIt 2 (and PyMoveIt2 for the Python side) to plan and execute trajectories

## Project layout

```
panda_bringup/       launch files that bring the whole system up
panda_controller/    joint and gripper controller config
panda_description/   the robot's URDF, meshes, and Gazebo world
panda_moveit/        MoveIt 2 config (SRDF, kinematics, controllers)
panda_vision/        the OpenCV color detection node
pymoveit2/           Python MoveIt 2 interface + the pick-and-place script
```

## How to run it

You'll need Ubuntu 22.04 with ROS 2 Humble. If you don't have that set up yet, follow the official [ROS 2 Humble install guide](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html) first.

**1. Install the extra dependencies**

```bash
sudo apt install -y \
  ros-humble-moveit \
  ros-humble-moveit-ros-move-group \
  ros-humble-moveit-ros-planning-interface \
  ros-humble-moveit-visual-tools \
  ros-humble-ros2-control \
  ros-humble-ros2-controllers \
  ros-humble-gazebo-ros2-control \
  ros-humble-ros-gz \
  ros-humble-cv-bridge \
  ros-humble-image-transport

pip3 install --no-cache-dir opencv-python==4.10.0.84 numpy==1.24.4 transforms3d
```

**2. Build the workspace**

```bash
mkdir -p ~/panda_ws/src
cd ~/panda_ws/src
git clone https://github.com/romi-rk/portfolio.git tmp_clone
cp -r tmp_clone/07-ros2-franka-panda-color-sorting/* . && rm -rf tmp_clone

cd ~/panda_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build
source install/setup.bash
```

**3. Run it**

Open two terminals.

Terminal 1, bring up the simulation:
```bash
source ~/panda_ws/install/setup.bash
ros2 launch panda_bringup pick_and_place.launch.py
```
Give it a bit to load Gazebo and RViz.

Terminal 2, start the pick-and-place logic:
```bash
source ~/panda_ws/install/setup.bash
ros2 run pymoveit2 pick_and_place.py --ros-args -p target_color:=R
```
Swap `R` for `G` or `B` to sort a different color.

Note: this needs Ubuntu 22.04 since ROS 2 Humble doesn't install natively on Windows or macOS. WSL2 or a VM works fine if that's what you're on.

## Useful commands while debugging

```bash
ros2 node list
ros2 topic list
ros2 topic echo /detected_color
ros2 run rqt_graph rqt_graph
```

## References I used

- [ROS 2 Humble docs](https://docs.ros.org/en/humble/)
- [MoveIt 2 docs](https://moveit.picknik.ai/humble/index.html)
- [PyMoveIt2](https://github.com/AndrejOrsula/pymoveit2), the Python MoveIt 2 wrapper this project is built on
- [Franka Emika docs](https://frankaemika.github.io/)
- [Gazebo docs](https://gazebosim.org/)

## License

MIT, see the [LICENSE](pymoveit2/LICENSE) file.