# -*- coding: utf-8 -*-
"""
Rekognitionで顔の判別をするAPIにアクセスするコード
引数1: Rekognitionで判別させたい顔が映った画像のS3ファイル名
引数2: Rekognitionで判別させたい顔が映った画像が格納されているS3バケット名
引数3: 顔の類似度の信頼度(%)
"""
import sys
import urllib.request
import json
import ssl #認証方法をTLSv1に指定
# import rekognition_data_formatter
import subprocess

# このファイルを実行時に受け取る引数
ARGS = sys.argv
# APIキーの指定
API_KEY =  'xxxxxxxxxxxxxxxxxxx'
# APIのステージ
STAGE = 'xxxxxx'
# APIのID
API_ID = 'xxxxxx'
# APIのリソースパス
RESOURCE = 'xxxxxx'
BASE_URL = 'https://{api_id}.execute-api.ap-northeast-1.amazonaws.com/{stage}/{resource}'

# step4で作成するログ送信用プログラムのパス
# PUB_AUTH_LOG_PATH = '../step4/pub_auth_log_data.py' 
class Api():
     def __init__(self):
          self.api_key = API_KEY
          self.api_id = API_ID
          self.stage = STAGE
          self.resource = RESOURCE
          self.base_url = BASE_URL
          self.file_name = ARGS[1]
          self.bucket_name = ARGS[2]
          self.threshold = ARGS[3]

     def create_url(self):
          """
          APIのURLを作成する
          """
          return BASE_URL.format(api_id=API_ID, stage=STAGE, resource=RESOURCE)

     def create_header(self):
          """
          POSTリクエスト時に利用するヘッダーを作成
          """
          return {
               'Content-type': 'application/json',
               'x-api-key': API_KEY
          }

     def create_body(self):
          """
          POSTリクエスト時に利用するボディを作成
          """
          data = {
               'file_name': self.file_name,
               'bucket_name': self.bucket_name,
               'threshold': self.convert_to_float(self.threshold)
          }
          return self.convert_to_json(data)
 
          
     def convert_to_float(self, data):
          """
          受け取ったオブジェクトをFloat型にする
          """
          return float(data)


     def convert_to_json(self, data):
          """
          受け取ったオブジェクトをJSON化する
          """
          return json.dumps(data)

     
     # def call_pub_auth_log_data(self, format_data):
     #      for data in format_data:
     #           subprocess.call(["python3", PUB_AUTH_LOG_PATH, json.dumps(data)])

     # def write_log(self, format_result, format_data):
     #      with open('create_auth_log.log', 'w') as f:
     #           f.write(str(format_result) + ',\n' + json.dumps(format_data))

     def post_request(self):
          """
          urllib.requestモジュールで指定のURLにデータをPOSTする
          """
          # SSLをTLSv1方式にする
          context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
          try:
               request_data = urllib.request.Request(
                    self.create_url(),
                    self.create_body().encode(),
                    self.create_header(),
                    )
               with urllib.request.urlopen(request_data,context=context) as response_data:
                    response = response_data.read().decode()

                    # 2-5-4で使用するAPIレスポンスの加工処理
                    # response_json = json.loads(response)
                    # format_result, format_data = rekognition_data_formatter.format_auth_log_data(json.dumps(response_json['payloads']), self.file_name)
                    
                    # 2-5-5で使うログ出力
                    # if format_data != None:
                    #    self.write_log(format_result, format_data)

                    # step4の関数を呼び出す処理
                    # if format_data != []:
                    #    self.call_pub_auth_log_data(format_data)

          except Exception as error:
               response = '[FAILED]{}'.format(error)
          finally:
               return self.print_response(response)

     def print_response(self, response):
          """
          コンソールに出力する
          """
          print(response)

#　初期化
api = Api()

if __name__ == "__main__":
     api.post_request()


