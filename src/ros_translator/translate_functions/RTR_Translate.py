# IS
from is_wire.core import Status, StatusCode, Logger
from is_msgs.robot_pb2 import RobotTaskRequest 
from is_wire.rpc import ServiceProvider, LogInterceptor
from is_msgs.common_pb2 import Position

# ROS
import roslibpy
from move_base_msgs.msg import MoveBaseActionGoal
from rospy_message_converter import message_converter
from dynamic_reconfigure.srv import Reconfigure
from dynamic_reconfigure.msg import Config, BoolParameter

# MSG Translations
from .msg_translations import *

def RTR_Translate(ros_tr, translate_request):
    logger = Logger('RTR_Translate')

    ros_topic = translate_request.topic
    task_request = RobotTaskRequest()
    translate_request.any.Unpack(task_request)

    # Allowed_Error
    if task_request.basic_move_task.allowed_error != '':
        changes_json = AllowedError_to_Config(task_request.basic_move_task.allowed_error)
        call_service = ros_tr.ros_service('/move_base/DWAPlannerROS/set_parameters', Reconfigure, changes_json)
    else: logger.warn('Allowed_Error not specified. Proceeding with current allowed_error.')

    # Position and Orientation
    mbag_standard = MoveBaseActionGoal()
    mbag_standard.goal.target_pose.header.frame_id = "map"

    # # Orientation
    if task_request.basic_move_task.HasField('final_orientation'):
        mbag_standard.goal.target_pose.pose.orientation = Orientation_to_Quartenion(task_request.basic_move_task.final_orientation)
    else: logger.warn('Final orientation not specified. Proceeding with (roll, pitch, yaw) = (0, 0, 0).')

    # # Position
    if len(task_request.basic_move_task.positions) != 0:
        goal_id = 0
        set_orientation_allowed_error(ros_tr, 10)
        for step in task_request.basic_move_task.positions:
            if step == task_request.basic_move_task.positions[-1]:
                set_orientation_allowed_error(ros_tr, 0.1)

            goal_id = goal_id +1
            mbag_standard.goal_id.id = str(goal_id)

            logger.info("New goal (x, y, z):  ({}, {}, {})".format(step.x, step.y, step.z))
            mbag_standard.goal.target_pose.pose.position = Position_to_Point(step)
            mbag_json = message_converter.convert_ros_message_to_dictionary(mbag_standard)
            ros_tr.ros_topic_publisher(ros_topic, 'move_base_msgs/MoveBaseActionGoal', mbag_json)
            verify_goal_achievement(ros_tr, goal_id)

    else: logger.warn('Positions not specified. Proceeding with current position.')

    mbag_json = message_converter.convert_ros_message_to_dictionary(mbag_standard)

    message_type = 'move_base_msgs/MoveBaseActionGoal'
    pub = ros_tr.ros_topic_publisher(translate_request.topic, message_type, mbag_json)

    return Status(StatusCode.OK)


def set_orientation_allowed_error(ros_tr, allowed_error):
    changes = Config()
    bool_p = BoolParameter()
    bool_p.name = 'yaw_goal_tolerance'
    bool_p.value = allowed_error
    changes.doubles = [bool_p]
    changes_json = message_converter.convert_ros_message_to_dictionary(changes)
    changes_json = {"config": changes_json}
    call_service = ros_tr.ros_service('/move_base/DWAPlannerROS/set_parameters', Reconfigure, changes_json)

def verify_goal_achievement(ros_tr, goal_id):
    verify = ros_tr.ros_topic_subscriber('/move_base/status', 'actionlib_msgs/GoalStatusArray')
    while len(verify['status_list']) < 1:
        verify = ros_tr.ros_topic_subscriber('/move_base/status', 'actionlib_msgs/GoalStatusArray')
    while verify['status_list'][0]['goal_id']['id'] != str(goal_id):
        verify = ros_tr.ros_topic_subscriber('/move_base/status', 'actionlib_msgs/GoalStatusArray')
    while verify['status_list'][0]['status'] == 1:
        verify = ros_tr.ros_topic_subscriber('/move_base/status', 'actionlib_msgs/GoalStatusArray')