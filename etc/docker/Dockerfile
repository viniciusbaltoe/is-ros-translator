FROM ros:noetic as package_step

RUN apt-get update

WORKDIR /opt/ros_translator
COPY ./requirements.txt .

RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt
RUN pip install --upgrade protobuf

# ROS Settings
RUN apt install -y ros-noetic-move-base 
RUN apt install -y ros-noetic-tf

# Provisório
COPY ./etc ./etc 
COPY ./src ./src
WORKDIR /opt/ros_translator/src


