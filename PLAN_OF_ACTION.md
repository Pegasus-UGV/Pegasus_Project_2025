# Pegasus - Sofrware - Plan of Action

1. Install the latest release of Ubuntu LTS on the nvidia jetson. You can choose to install or not install the desktop software, we should have enough space on the SD card to install Ubuntu's GUI. If we choose to go down this path, we will likely be doing most of the development/visualization on the Jetson itself. 
We can also consider just installing Jetson OS, which is a variant of Ubuntu with all the jetson specific stuff and configs pre loaded
https://developer.nvidia.com/embedded/jetson-linux#:~:text=NVIDIA%20Jetson%20Linux%2036.4.&text=4-,Jetson%20Linux%2036.4.,Developer%20Guide%20for%20detailed%20documentation.

2) Install a Wi-Fi card into the Jetson's M.2 port.
3) Connect to maglab's internet via the jetson's ethernet
4) Go into root mode (the sudo[s] afterr here are redundant but whatever)
```bash
sudo bash
```
5) Install the ROS things (this variant of the script is meant specifically if the GUI is installed)
```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
sudo apt install ros-humble-desktop
sudo apt install ros-dev-tools
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```
6) Install nav2 + SLAM
```bash
sudo apt install ros-humble-slam-toolbox
sudo apt install ros-humble-navigation2

```
7)  Immidiately set up SSH and use `netplan` to configure the device's networking. The software stack that the employees will use to control the robot
