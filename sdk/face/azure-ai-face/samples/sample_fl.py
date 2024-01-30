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
from azure.core.credentials import AzureKeyCredential
from azure.ai.face import FaceClient
from azure.ai.face.models import FaceList
from dotenv import find_dotenv, load_dotenv

TEST_DEVICE_CORELATION_ID = "dummy-test-id"
TEST_LIVENESS_OPERATION_MODE = "Passive"

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    endpoint = os.environ["FACE_ENDPOINT"]
    key = os.environ["FACE_KEY"]

    client = FaceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    operations = client.face_lists

    lid = "my_list"

    try:
        operations.delete_list(lid)
    except:
        pass

    result = operations.create_list(lid, FaceList(name="my list name"))
    print(result)

    result = operations.add_face_from_url(
        lid,
        body={
            "url": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/detection1.jpg"
        },
    )
    print(result)
    face_id = result.persisted_face_id

    result = operations.list_list()
    print(result)

    result = operations.update_list(lid, FaceList(name="new name"))
    print(result)

    result = operations.get_list(lid)
    print(result)

    fid = client.detect_from_url(
        url="https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/detection1.jpg"
    )[0].face_id

    result = operations.find_similar_from_face_list(face_id=fid, face_list_id=lid)
    print(result)

    result = operations.delete_face(lid, face_id)
    print(result)

    result = operations.delete_list(lid)
    print(result)
