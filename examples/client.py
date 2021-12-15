from is_msgs.robot_pb2 import RobotTaskRequest, RobotTaskReply
from is_wire.core import Channel, Subscription, Message
from is_msgs.common_pb2 import Position
from is_ros_pb2 import ROSTranslateRequest, ROSTranslateReply

from google.protobuf.empty_pb2 import Empty
from google.protobuf.any_pb2 import Any

import json
import socket
import time

if __name__ == "__main__":
# -------------------------- Options ------------------------- 
    cont = True
    config_file = '../etc/conf/config.json'
    config = json.load(open(config_file, 'r'))    
    channel = Channel(config["broker_uri"])
    robot_config = config["robot"]
    subscription = Subscription(channel)

# ---------------------- Get Info ------------------------
    topic = "ROSTranslator.{}.GetInfo".format(robot_config["robot_id"])
    print("Publishing to topic: {}".format(topic))
    
    ros_request = ROSTranslateRequest()
    #ros_request.topic = '/odom'

    channel.publish(
        Message(content=ros_request, reply_to=subscription),
        topic=topic)

    try:
        reply = channel.consume(timeout=3.0)
        unpacked_msg = reply.unpack(ROSTranslateReply)
        print('INFO:\n', unpacked_msg.data, '\n')
    except socket.timeout:
        print('No reply to Get 1 :(')

# ---------------------- Translate Request -------------------
    topic = "ROSTranslator.{}.Translate".format(robot_config["robot_id"])
    print("Publishing to topic: {}".format(topic))

    rt_request = RobotTaskRequest()
    rt_request.id = 10
    rt_request.basic_move_task.positions.extend([Position(x=1.5, y=1.5, z=0)])
    rt_request.basic_move_task.positions.extend([Position(x=1.5, y=-1.5, z=0)])
    rt_request.basic_move_task.positions.extend([Position(x=-1.5, y=-1.5, z=0)])
    rt_request.basic_move_task.positions.extend([Position(x=-1.5, y=1.5, z=0)])

    rt_request.basic_move_task.final_orientation.yaw = 0.0
    rt_request.basic_move_task.final_orientation.pitch = 0.0
    rt_request.basic_move_task.final_orientation.roll = 0.0

    rt_request.basic_move_task.allowed_error = 0.1
    
    ros_request = ROSTranslateRequest()
    ros_request.any.Pack(rt_request)
    ros_request.topic = '/move_base/goal'

    channel.publish(
        Message(content=ros_request, reply_to=subscription),
        topic=topic)
    try:
        reply = channel.consume()
        unpacked_msg = reply.unpack(ROSTranslateReply)
        print('RPC Status: {}'.format(reply.status))
    except socket.timeout:
        print('No reply to RobotTaskRequest :(')

# ---------------------- Get Info ------------------------
    topic = "ROSTranslator.{}.GetInfo".format(robot_config["robot_id"])
    print("Publishing to topic: {}".format(topic))
    
    ros_request = ROSTranslateRequest()
    ros_request.topic = '/odom'

    channel.publish(
        Message(content=ros_request, reply_to=subscription),
        topic=topic)

    try:
        reply = channel.consume(timeout=3.0)
        unpacked_msg = reply.unpack(ROSTranslateReply)
        print('INFO:\n', unpacked_msg.data, '\n')
    except socket.timeout:
        print('No reply to Get 1 :(')
    