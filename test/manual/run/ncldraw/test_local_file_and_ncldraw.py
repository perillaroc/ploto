# coding=utf-8
import time
import json
import os

from kafka import KafkaClient, KafkaProducer
from kafka.errors import KafkaError


def main():
    producer = KafkaProducer(
        bootstrap_servers=['{kafka_host}:{kafka_port}'.format(
            kafka_host='localhost',
            kafka_port=9092)
        ]
    )

    kafka_topic = "gidat-plot"
    message = {
        'app': 'gidat-plot',
        'type': 'gidat-plot',
        'timestamp': time.time(),
        'data': {
            'files': [
                # {
                #     "type": "ftp",
                #     "host": "10.28.32.114",
                #     "user": "wangdp",
                #     "password": "perilla",
                #     "directory": "/srv/files/ftp/GRAPES_GFS_ORIG_2017070400",
                #     "file_name": "gmf.gra.2017070400009.grb2"
                # },
                {
                    "type": "local",
                    "directory": "/space/windroc/workspace/plot/playground/test_case_1",
                    "file_name": "data.grb2"
                },
                # {
                #     'type': 'ddps',
                #     'query_param': {
                #         "username": "admin",
                #         "password": "admin",
                #         "operation": "extractdownload",
                #         "config": {
                #             "date": "20140101",
                #             "groupname": "DYN",
                #             "expID": "G1600010",
                #             "time": "1200,12:00",
                #             "step": "0",
                #             "levtype": "pl",
                #             "param": "t",
                #             "levelist": "850",
                #             "savePath": "./ddps"
                #         }
                #     },
                #     'file_name': 'data_file.grib2'
                # }
            ],
            'plotter': {
                'type': 'ncldraw_plotter',
                'task_file': os.path.join(os.path.dirname(__file__), "task.xml"),
                'time_level': '2017071400084',
                'image_path': 'image.png',
            }
        }
    }

    message_string = json.dumps(message)
    print(message_string)
    future = producer.send(kafka_topic, message_string.encode('utf-8'))
    producer.flush()
    # Block for 'synchronous' sends
    try:
        record_metadata = future.get(timeout=10)
        print(record_metadata.topic)
        print(record_metadata.partition)
        print(record_metadata.offset)
    except KafkaError:
        # Decide what to do if produce request failed...
        pass

    return {'status': 'ok'}


if __name__ == "__main__":
    main()