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
from azure.ai.face.models import LargePersonGroup, LargePersonGroupPerson, LargePersonGroupPersonFace, RecognitionModel
from dotenv import find_dotenv, load_dotenv

TEST_DEVICE_CORELATION_ID = "dummy-test-id"
TEST_LIVENESS_OPERATION_MODE = "Passive"

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    endpoint = os.environ["FACE_ENDPOINT"]
    key = os.environ["FACE_KEY"]

    client = FaceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    operations = client.large_person_groups

    gid = "my_lpg"

    try:
        operations.delete_group(gid)
    except:
        pass

    result = operations.create_group(gid, LargePersonGroup(name="my lpg name"))
    print(result)

    result = operations.create_person(gid, LargePersonGroupPerson(name="person1"))
    print(result)
    pid = result.person_id

    result = operations.add_face_from_url(
        gid,
        pid,
        body={
            "url": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/detection1.jpg"
        },
    )
    print(result)
    face_id = result.persisted_face_id

    result = operations.list_group()
    print(result)

    result = operations.list_person(gid)
    print(result)

    result = operations.update_group(gid, LargePersonGroup(name="new name"))
    print(result)

    result = operations.get_group(gid)
    print(result)

    result = operations.update_person(gid, pid, LargePersonGroupPerson(name="new name"))
    print(result)

    result = operations.get_person(gid, pid)
    print(result)

    result = operations.update_face(gid, pid, face_id, LargePersonGroupPersonFace(user_data="new face data"))
    print(result)

    result = operations.get_face(gid, pid, face_id)
    print(result)

    result = operations.train_group(gid)
    print(result)

    result = operations.get_group_training_status(gid)
    print(result)

    fids = [
        client.detect_from_url(
            url="https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/detection1.jpg"
        )[0].face_id
        for _ in range(3)
    ]

    result = operations.identify_from_large_person_group(face_ids=fids, large_person_group_id=gid)
    print(result)

    result = operations.verify_from_large_person_group(face_id=fids[0], large_person_group_id=gid, person_id=pid)
    print(result)

    result = operations.delete_face(gid, pid, face_id)
    print(result)

    result = operations.delete_person(gid, pid)
    print(result)

    result = operations.delete_group(gid)
    print(result)
