# -*- coding: utf-8 -*-
"""
ドアオープンのログをクラウドにアップロードするコード
引数1: ドアオープン時の対象者
"""
import sys
import json
import boto3
import datetime

# ----- 定数 -----
# このファイルを実行時に受け取る引数(JSON)
ARGS = sys.argv

class PubDoorOpenLogData():
    def __init__(self):
        self.arg_door_open_person = ARGS[1]

    def get_now_datetime(self):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        return timestamp

    def create_json_data(self, timestamp):
        log_data_json = {
                                "DeviceID": "id001",
                                "Datetime": timestamp,
                                "Person": self.arg_door_open_person
                            }
        return json.dumps(log_data_json)

    def publish_door_open_log_data(self, log_data):
        iot_data = boto3.client('iot-data')
        response = iot_data.publish(
                topic='handson/doorOpenLogData',
                qos = 1,
                payload = log_data
        )
        print(response)
    
    def main(self):
        try:
            #self.publish_door_open_log_data()
            timestamp = self.get_now_datetime()
            log_data = self.create_json_data(timestamp)
            self.publish_door_open_log_data(log_data)

        except Exception as error:
            print(error)

#　初期化
pub_door_open_log_data = PubDoorOpenLogData()

if __name__ == "__main__":
    pub_door_open_log_data.main()
