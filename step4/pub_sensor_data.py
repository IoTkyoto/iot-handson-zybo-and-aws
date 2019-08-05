# -*- coding: utf-8 -*-
"""
センサー値をクラウドにアップロードするコード
引数1: センサー値のリアルタイムデータ(JSON)
"""
import sys
import json
import boto3
import datetime

# ----- 定数 -----
# このファイルを実行時に受け取る引数(str型)
ARGS = sys.argv

class PubSensorData():
    def __init__(self):
        self.arg_sensor_data = ARGS[1]

    def get_now_datetime(self):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        return timestamp

    def create_json_data(self, timestamp):
        sensor_data_json = {
                                "DeviceID": "id001",
                                "Datetime": timestamp,
                                "Value": int(self.arg_sensor_data)
                            }
        return json.dumps(sensor_data_json)

    def publish_sensor_data(self, sensor_data):
        iot_data = boto3.client('iot-data')
        response = iot_data.publish(
                topic='handson/sensorLogData',
                qos = 1,
                payload = sensor_data
        )
        print(response)
    
    def main(self):
        try:
            timestamp = self.get_now_datetime()
            sensor_data = self.create_json_data(timestamp)
            self.publish_sensor_data(sensor_data)
        except Exception as error:
            print(error)

#　初期化
pub_sensor_data = PubSensorData()

if __name__ == "__main__":
    pub_sensor_data.main()
