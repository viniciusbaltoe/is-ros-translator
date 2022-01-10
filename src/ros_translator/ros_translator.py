# ROS
import roslibpy

# Tranlate functions
from .translate_functions import *

# Python
import sys
import time
import json
import math
import socket

# IS
from is_wire.core import Channel, Message, Logger, Status, StatusCode
from .is_ros_pb2 import ROSTranslateRequest, ROSTranslateReply
from is_wire.rpc import ServiceProvider, LogInterceptor
from google.protobuf.any_pb2 import Any


def get_obj(callable, obj):
    value = callable()
    if value is not None:
        obj.CopyFrom(value)

def get_val(callable, obj, attr):
    value = callable()
    if value is not None:
        setattr(obj, attr, value)

def get_class( kls ):
    kls = kls.replace('is', 'is_msgs')
    kls = kls.replace('camera', 'camera_pb2')
    kls = kls.replace('common', 'common_pb2')
    kls = kls.replace('image', 'image_pb2')
    kls = kls.replace('power', 'power_pb2')
    kls = kls.replace('robot', 'robot_pb2')
    kls = kls.replace('tests', 'tests_pb2')
    kls = kls.replace('validate', 'validate_pb2')

    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m

class ROSTranslator(object):
    def __init__(self, robot_config, correspondence_dict):
        self.logger = Logger("ROSTranslator")

        self.robot_id = robot_config['robot_id']
        self.robot_ip = robot_config['robot_ip']
        self.robot_port = robot_config['robot_port']

        self.correspondence = correspondence_dict

        self.ros = roslibpy.Ros(host=str(self.robot_ip), port=int(self.robot_port))
        self.ros.run()

# -=-=-=-=-=-=-=-=-=-=-= ROS TOPICS, SERVICES ... =-=-=-=-=-=-=-=-=-=-=-=-
    def ros_topic_publisher(self, ros_topic, message_type, message_json):
        publisher = roslibpy.Topic(self.ros, ros_topic, message_type,  queue_size=10, latch=True)
        for i in range(1,11): 
            publisher.publish(roslibpy.Message(message_json))
        publisher.unadvertise()

    def ros_topic_subscriber(self, ros_topic, message_type):
        self.listener = roslibpy.Topic(self.ros, ros_topic, message_type)
        self.listener.subscribe(lambda message: self.subscriber_callback(message))
        while self.listener.is_subscribed: time.sleep(1)
        return self.subscriber_data # return json

    def subscriber_callback(self, message):
        self.subscriber_data = message
        self.listener.unsubscribe()

    def ros_topic_list(self):
        return self.ros.get_topics()
    
    def ros_topic_msg_type(self, ros_topic):
        return self.ros.get_topic_type(ros_topic)

    def ros_service(self, ros_service, message_type, message_json=None):
        service = roslibpy.Service(self.ros, ros_service, message_type)
        request = roslibpy.ServiceRequest(message_json)
        result = service.call(request)

# -=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    def get_info(self, translate_request, ctx):
        translate_reply = ROSTranslateReply()
        if translate_request.topic == '':
            translate_reply.data = str(self.ros_topic_list())
            return translate_reply
        msg_type = self.ros.get_topic_type(translate_request.topic) # return string
        translate_reply.data = str(self.ros_topic_subscriber(translate_request.topic, msg_type))
        return translate_reply

    def translate(self, translate_request, ctx):
        
        if translate_request.topic == '':
            topics = self.ros_topic_list()
            return Status(StatusCode.CANCELLED,
                    why='No topic received. List of available topics: {}'.format(topics))

        is_msg_type_class = get_class(translate_request.any.type_url.split('/')[-1])
        is_msg = is_msg_type_class()
        translate_request.any.Unpack(is_msg)

        if translate_request.function == '':
            method_name = self.correspondence[translate_request.any.type_url.split('/')[-1].split('.')[-1]]
        else:
            method_name = translate_request.function

        funcs = globals().copy()
        funcs.update(locals())
        method = funcs.get(method_name)
        if not method:
             raise NotImplementedError("Method/Function %s not implemented" % method_name)
        function = getattr(method, method_name)
        maybe_ok = function(self, translate_request)

        if maybe_ok != Status(StatusCode.OK):
            return maybe_ok

        return Status(StatusCode.OK)


    def run(self,broker_uri):
        service_name = "ROSTranslator.{}".format(self.robot_id)

        publish_channel = Channel(broker_uri)
        rpc_channel = Channel(broker_uri)
        server = ServiceProvider(rpc_channel)
        logging = LogInterceptor()
        server.add_interceptor(logging)
        
        server.delegate(
            topic=service_name + ".GetInfo",
            request_type=ROSTranslateRequest,
            reply_type=ROSTranslateReply,
            function=self.get_info)
        
        server.delegate(
            topic=service_name + ".Translate",
            request_type=ROSTranslateRequest,
            reply_type=ROSTranslateReply,
            function=self.translate)

        self.logger.info("RPC listening for requests")
        while True:
            try:
                message = rpc_channel.consume(timeout=0)
                if server.should_serve(message):
                    server.serve(message)
            except socket.timeout:
                pass
        rospy.spin()

