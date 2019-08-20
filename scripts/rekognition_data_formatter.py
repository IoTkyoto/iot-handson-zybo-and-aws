# -*- coding: utf-8 -*-
"""
渡されたデータを加工するスクリプト
"""

import sys
import json

def format_auth_log_data(ARGS_DATA, ARGS_AUTH_PICTURE_NAME):
    """
    顔認証APIのレスポンスを分かりやすい形にフォーマットする
    """
    try:
        auth_log_data = []
        auth_result = None
        ARGS_DATA = json.loads(ARGS_DATA)
        if ARGS_DATA['FaceMatches'] != []:
            for data in ARGS_DATA['FaceMatches']:
                auth_log_data.append({
                    "DeviceID": "id001",
                    "Datetime": ARGS_DATA['timestamp'],
                    "AuthenticationResult": True,
                    "PictureName": ARGS_AUTH_PICTURE_NAME,
                    "Person": data['Face']['ExternalImageId']
                })
            auth_result = True
        else:
            auth_log_data.append({
                "DeviceID": "id001",
                "Datetime": ARGS_DATA['timestamp'],
                "AuthenticationResult": False,
                "PictureName": ARGS_AUTH_PICTURE_NAME,
            })
            auth_result = False
        return auth_result, auth_log_data
    except Exception as error:
        print(error)
        return False, []


def format_analysis_log_data(ARGS_DATA):
    """
    顔分析APIのレスポンスを分かりやすい形にフォーマットする
    """
    try:
        rekognition_data = []
        ARGS_DATA = json.loads(ARGS_DATA)
        for data in ARGS_DATA['analysis']:
            rekognition_data.append({
                'Datetime': ARGS_DATA['timestamp'],
                'AgeRange-Low': data['AgeRange']['Low'],
                'AgeRange-High': data['AgeRange']['High'],
                'Gender': data['Gender']['Value'],
                'Smile': data['Smile']['Value'],
                'Eyeglasses': data['Eyeglasses']['Value'],
                'Sunglasses': data['Sunglasses']['Value'],
                'Beard': data['Beard']['Value'],
                'Mustache': data['Mustache']['Value'],
                'EyesOpen': data['EyesOpen']['Value'],
                'MouthOpen': data['MouthOpen']['Value']
            })
        return rekognition_data
    except Exception as error:
        print(error)
        return []