# -*- coding: utf-8 -*-
"""
コマンドライン引数として渡した画像データをS3のバケットへ入れる
以下のpythonを実行 "$ python {第一引数} {第二引数} {第三引数}"
また {第一引数} にはpythonファイル(例: s3_upload.py),
{第二引数} にはローカルの画像が置いてあるファイルパス(例: ../Desktop/picture/Taro_Yamada.jpg),
{第三引数} にはS3のバケット名を指定(例: target-faces-handson)
"""

# ----- インポート -----
import json
import sys
from datetime import datetime as dt
import os
import boto3
import botocore
from botocore.exceptions import ClientError
import gc

# ----- 定数 -----
DATA_NOW = dt.now()
TIMESTAMP = str(DATA_NOW.strftime('_%Y%m%d%H%M%S')) #日本時間

# ----- 変数(グローバル) -----
args = sys.argv                 # コマンドライン引数用
filepath = args[1]              # あげる画像のファイルパス

# ----- クラス -----
class Relation_s3:
    # 変数
    bucketname = ""               # S3にアップロード時の名前
    s3 = None
    bucket = None

    # 関数
    # アップロードする時の名前
    def upload_name(self):
        # ディレクトリ名とファイル名を分ける
        directory, filename = os.path.split(filepath)
        # ファイル名の拡張子前後で分ける
        current_file_name, extension = os.path.splitext(filename)
        # ファイル名の後にタイムスタンプを追記しその後に拡張子が来るようにする
        relation_s3.bucketname = current_file_name + TIMESTAMP + extension

    # S3に画像をあげる
    def upload(self):
        try:
            # S3にあげる(第一引数: あげるファイルパス(コマンドライン引数), 第二引数: S3に作られるファイル名)
            relation_s3.bucket.upload_file(filepath, relation_s3.bucketname)
        except FileNotFoundError:
            print('[file not found]')
        except boto3.exceptions.S3UploadFailedError as e:
            print('[upload failed]' + str(e))    
        except Exception as e:
            print('[error]' + str(e))  
        else:
            print('succeeded!')

    # クレデンシャル 
    def credentials(self):
        # リソース指定(クレデンシャル)
        relation_s3.s3 = boto3.resource('s3')
        # S3のバケット名指定(args[2]: コマンドライン引数で第二引数として渡した名前)
        relation_s3.bucket = relation_s3.s3.Bucket(args[2])

# ----- メイン -----
if __name__ == '__main__':

    # クラスのコンストラクタ
    relation_s3 = Relation_s3()

    print("")

    # S3にアップロードする時の名前
    relation_s3.upload_name()

    # リソース指定(クレデンシャル)
    relation_s3.credentials()

    # S3に画像をあげる
    try:
        relation_s3.upload()
    except Exception as e:
        print(e)

    # アップロード時のファイル名を表示
    print("upload file name: " + str(relation_s3.bucketname))

    print("")

    # メモリ解放
    del relation_s3
    gc.collect()