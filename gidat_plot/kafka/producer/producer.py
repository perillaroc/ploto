# coding=utf-8
import time
import json

from kafka import KafkaClient, KafkaProducer
from kafka.errors import KafkaError


def get_ncl_script():
    return """begin
    f = addfile(file_path,"r")

    var = f->TMP_P0_L1_GLL0

    wks = gsn_open_wks("png", image_path)

    res = True
    res@tiMainString = "TEMP"
    res@cnFillOn = True

    plot = gsn_csm_contour_map(wks,var,res)

end
"""


def main():
    producer = KafkaProducer(
        bootstrap_servers=['{kafka_host}:{kafka_port}'.format(
            kafka_host='10.28.32.114',
            kafka_port=9092)
        ]
    )

    kafka_topic = "gidat_plot"
    message = {
        'app': 'gidat_plot',
        'type': 'gidat_plot',
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
                    "host": "10.28.32.114",
                    "user": "wangdp",
                    "password": "perilla",
                    "directory": "/srv/files/ftp/GRAPES_GFS_ORIG_2017070400",
                    "file_name": "gmf.gra.2017070400009.grb2"
                },
            ],
            'plotter': {
                'type': 'ncl_plotter',
                'ncl_script_content': get_ncl_script(),
                'image_path': 'image.png',
                'ncl_params': 'file_path=\\"{file_path}\\" image_path=\\"{image_path}\\"'.format(
                    file_path='gmf.gra.2017070400009.grb2',
                    image_path='image.png'
                ),
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
