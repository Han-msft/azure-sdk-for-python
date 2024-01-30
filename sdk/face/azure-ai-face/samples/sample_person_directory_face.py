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
from azure.ai.face.models import PersonDirectoryPerson, RecognitionModel
from dotenv import find_dotenv, load_dotenv

TEST_DEVICE_CORELATION_ID = "dummy-test-id"
TEST_LIVENESS_OPERATION_MODE = "Passive"

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    endpoint = os.environ["FACE_ENDPOINT"]
    key = os.environ["FACE_KEY"]

    client = FaceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    operations = client.person_directory_persons

    person = PersonDirectoryPerson(name="Person1")
    poller = operations.begin_create_person(resource=person)
    result = poller.result()
    print(result)
    pid = result.person_id

    result = operations.list_person()
    print(result)

    person = PersonDirectoryPerson(name="NewName")
    result = operations.update_person(pid, person)
    print(result)

    result = operations.get_person(pid)
    print(result)

    poller = operations.begin_add_face_from_url(
        pid,
        RecognitionModel.RECOGNITION_04,
        {
            "url": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/detection1.jpg"
        },
    )
    result = poller.result()
    print(result)
    fid = result.persisted_face_id

    result = operations.list_face(pid, RecognitionModel.RECOGNITION_04)
    print(result)

    result = operations.update_face(pid, RecognitionModel.RECOGNITION_04, fid, {"userData": "new face user data"})
    print(result)

    result = operations.get_face(pid, RecognitionModel.RECOGNITION_04, fid)
    print(result)

    pids = [pid]
    fids = [
        client.detect_from_url(
            url="https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/detection1.jpg",
            recognition_model=RecognitionModel.RECOGNITION_04,
        )[0].face_id
        for _ in range(3)
    ]

    result = operations.identify_from_person_directory(face_ids=fids, person_ids=pids)
    print(result)

    result = operations.verify_from_person_directory(face_id=fids[0], person_id=pids[0])
    print(result)

    poller = operations.begin_delete_face(pid, RecognitionModel.RECOGNITION_04, fid)
    result = poller.result()
    print(result)

    poller = operations.begin_delete_person(person_id=pid)
    print(poller.result())
