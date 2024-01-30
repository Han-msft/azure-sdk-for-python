# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_liveness_session.py

DESCRIPTION:
    This sample demonstrates how to manage the session for detect liveness.

USAGE:
    python sample_liveness_session.py

    Set the environment variables with your own values before running the sample:
    1) FACE_ENDPOINT - the endpoint to your Face resource.
    2) FACE_KEY - your Face API key.
"""

import os
from pathlib import Path
from azure.core.credentials import AzureKeyCredential
from azure.ai.face import FaceClient
from azure.ai.face.models import DetectionModel, RecognitionModel, CompareFromStreamContent
from dotenv import find_dotenv, load_dotenv

TEST_DEVICE_CORELATION_ID = "dummy-test-id"
TEST_LIVENESS_OPERATION_MODE = "Passive"

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    endpoint = os.environ["FACE_ENDPOINT"]
    key = os.environ["FACE_KEY"]

    client = FaceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/detection1.jpg"

    print(
        client.detect_from_url(
            url=image_url,
            return_face_id=False,
            return_face_attributes="headpose,mask,qualityforrecognition",
            return_face_landmarks=True,
            return_recognition_model=True,
            detection_model=DetectionModel.DETECTION_03,
            recognition_model=RecognitionModel.RECOGNITION_04,
        )
    )

    sample_path = Path(__file__).resolve().parent / "sample.jpg"
    with open(sample_path, "rb") as fd:
        file = fd.read()
    print(client.detect_from_stream(image_content=file, return_face_id=False))

    result = client.detect_from_url(url=image_url)
    print(result)
    fid = result[0].face_id

    fids = [client.detect_from_url(url=image_url)[0].face_id for _ in range(3)]

    result = client.find_similar(face_id=fid, face_ids=fids)
    print(result)

    result = client.verify(face_id1=fid, face_id2=fids[0])
    print(result)

    result = client.group(face_ids=fids)
    print(result)

    result = client.compare(source_image_url=image_url, target_image_url=image_url)
    print(result)

    result = client.compare_from_stream(CompareFromStreamContent(source=file, target=file))
    print(result)

