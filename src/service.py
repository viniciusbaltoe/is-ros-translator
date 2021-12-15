import sys
import json
from ros_translator.ros_translator import ROSTranslator


def main():
    config_file = sys.argv[1] if len(sys.argv) > 1 else '../etc/conf/config.json'
    config = json.load(open(config_file, 'r'))

    broker_uri = config['broker_uri']
    robot_config = config['robot']

    correspondence_dict_file = sys.argv[1] if len(sys.argv) > 1 else 'ros_translator/translate_functions/correspondence_dict.json'
    correspondence_dict = json.load(open(correspondence_dict_file, 'r'))

    service = ROSTranslator(robot_config=robot_config, correspondence_dict=correspondence_dict)
    service.run(broker_uri=broker_uri)

if __name__ == "__main__":
    main()