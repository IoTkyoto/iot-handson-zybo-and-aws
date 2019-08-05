# -*- coding: utf-8 -*-
"""
センサー値をクラウドにアップロードするコード
引数1: センサー値のリアルタイムデータ(JSON)
"""
import sys
import json
import boto3

# ----- 定数 -----
# このファイルを実行時に受け取る引数(JSON)
ARGS = sys.argv

class PubAuthLogData():
    def __init__(self):
        self.arg_auth_log_data = ARGS[1]

    def publish_auth_log_data(self):
        iot_data = boto3.client('iot-data')
        response = iot_data.publish(
                topic='handson/authLogData',
                qos = 1,
                payload = self.arg_auth_log_data
        )
        print(response)
    
    def main(self):
        try:
            self.publish_auth_log_data()
        except Exception as error:
            print(error)

#　初期化
pub_auth_log_data = PubAuthLogData()

if __name__ == "__main__":
    pub_auth_log_data.main()
