# -*- coding: utf-8 -*-
"""
Rekognitionのコレクションにアクセスし、登録されている顔かどうか認証するLambdaのためのコード
Method: POST
"""
import json
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

REKOGNITION_CLIENT = boto3.client('rekognition')
# Rekognitionで作成したコレクション名を入れてください
COLLECTION_ID = '{collection_id}'
# Rekognitionで一度に検出したい顔の最大数（最大4096人まで可）
MAX_FACES = 10

class Rekognition():
     def __init__(self):
          self.required_keys: list
          self.rekognition_client = REKOGNITION_CLIENT
          self.collection_id = COLLECTION_ID
          self.max_faces = MAX_FACES

     def convert_to_float(self, data) -> float:
          """
          受け取ったオブジェクトをFloat型にする
          """
          return float(data)
     
     def round_to_2nd_decimal(self, data) -> float:
          """
          受け取った数値を小数点第三位で四捨五入する
          """
          return round(data, 2)

     def make_timestamp(self) -> str: 
          """
          タイムスタンプを作成する
          """
          date_now = datetime.now()
          return str(date_now.strftime('%Y-%m-%d %H:%M:%S'))

     def create_response(self, data: dict):
          """
          Rekognition結果を解析し、Response Bodyのデータを作成する
          """
          payloads: dict = {}
          payloads['timestamp'] = self.make_timestamp()
          payloads.update(data)
          return make_response(200, '[SUCCEEDED]Rekognition done', payloads)

     def search_face(self, s3_bucket: str, s3_obj: str, threshold: float) -> dict:
          """
          画像とマッチする人物を特定する
          """
          try:
               search_result = REKOGNITION_CLIENT.search_faces_by_image(
                    CollectionId=self.collection_id,
                    Image={
                         'S3Object': {
                         'Bucket': s3_bucket,
                         'Name': s3_obj
                         }
                    },
                    MaxFaces=self.max_faces,
                    FaceMatchThreshold=threshold
               )
               return self.create_response(search_result)
          
          # S3アクセス時のエラーに対処
          except Exception as error:
               return make_response(400, '[FAILED]{}'.format(error))

     def check_validation(self, body: dict):
          """
          バリデーションチェックをする関数
          """
          if not isinstance(body, dict):
               return make_response(400, '[FAILED]Invalid body type')
          
          errors: list = []
          for key in self.required_keys:
               if not key in body.keys():
                    errors.append('key "{}" not found'.format(key))
               if body[key] == '':
                    errors.append('no value found for "{}"'.format(key))
               if key == 'bucket_name':
                    if not isinstance(body[key], str):
                         errors.append('invalid value type: "{}"'.format(body[key]))
               if key == 'file_name':
                    if not isinstance(body[key], str):
                         errors.append('invalid value type: "{}"'.format(body[key]))
               if key == 'threshold':
                    if not isinstance(body[key], (int, float)):
                         errors.append('invalid value type: "{}"'.format(body[key]))
          if errors:
               return make_response(400, '[FAILED]' + ', '.join(errors))
          else: 
               return

     def load_json(self, str_json: str) -> dict:
          """
          JSON文字列をPythonで処理できる形にする
          """
          if str_json is None:
               return make_response(400, '[FAILED]Data required')
          # Lambdaテスト時にdict型で入ってくるためif分岐
          if isinstance(str_json, str):
               # キー名がシングルクォーテーションで囲まれた場合jsonを変換できないためダブルクォーテーションに変換
               str_json = str_json.replace('\'', '"')
               return json.loads(str_json)
          else:
               return str_json

     def search_post(self, event):
          self.required_keys = ['bucket_name', 'file_name', 'threshold']
          
          body = self.load_json(event['body'])
          if 'statusCode' in body:
               return body
          validation_errors = self.check_validation(body)
          if validation_errors:
               return validation_errors

          search_result = self.search_face(body['bucket_name'], body['file_name'], body['threshold'])
          return search_result


def make_response(status_code: int, msg: str, payloads: dict = None):
          """
          レスポンスを作成する
          """
          if payloads:
               body = json.dumps({'msg': msg, 'payloads': payloads})
          else:
               body = json.dumps({'msg': msg})

          return {
               'statusCode': status_code,
               'body': body,
          }

#　初期化
rekognition = Rekognition()

def lambda_handler(event, _):
     """
     /searchに対するPOSTをトリガーに実行
     """
     try:
          return rekognition.search_post(event)
     except Exception as error:
          print('[DEBUG]: {}'.format(error))
          return make_response(500, '[FAILED]An error occurred : {}'.format(str(error)))
