
from geometry_msgs.msg import Quaternion, Point
from rospy_message_converter import message_converter
from dynamic_reconfigure.msg import Config, BoolParameter

from tf.transformations import euler_from_quaternion, quaternion_from_euler


# -=-=-=-=-=-=-=-=-=- Orientation -=-=-=-=-=-=-=-=-=-
def Orientation_to_Quartenion(orientation):
    orientation_q = Quaternion()
    robot_orientation_q = quaternion_from_euler(orientation.roll, orientation.pitch, orientation.yaw, 'sxyz')
    orientation_q.x = robot_orientation_q[0]
    orientation_q.y = robot_orientation_q[1]
    orientation_q.z = robot_orientation_q[2]
    orientation_q.w = robot_orientation_q[3]
    return orientation_q

# -=-=-=-=-=-=-=-=-=- Position -=-=-=-=-=-=-=-=-=-=-
def Position_to_Point(position):
    point = Point()
    point.x , point.y, point.z = position.x, position.y, position.z
    return point

# -=-=-=-=-=-=-=-=-=- AllowedError -=-=-=-=-=-=-=-=-
def AllowedError_to_Config(allowed_error):
    changes = Config()
    bool_p = BoolParameter()
    bool_p.name = 'xy_goal_tolerance'
    bool_p.value = allowed_error
    changes.doubles = [bool_p]
    changes_json = message_converter.convert_ros_message_to_dictionary(changes)
    return {"config": changes_json}