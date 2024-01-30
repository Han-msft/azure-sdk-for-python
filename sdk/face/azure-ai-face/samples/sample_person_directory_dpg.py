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
from azure.ai.face.models import PersonDirectoryPerson, DynamicPersonGroup, RecognitionModel
from dotenv import find_dotenv, load_dotenv

TEST_DEVICE_CORELATION_ID = "dummy-test-id"
TEST_LIVENESS_OPERATION_MODE = "Passive"

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    endpoint = os.environ["FACE_ENDPOINT"]
    key = os.environ["FACE_KEY"]

    client = FaceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    dpg_operations = client.person_directory_dynamic_person_groups
    person_operations = client.person_directory_persons

    gid = "my_dpg"

    try:
        poller = dpg_operations.begin_delete_group(gid)
        print(poller.result())
    except:
        pass

    poller = person_operations.begin_create_person(resource=PersonDirectoryPerson(name="Person1"))
    print(poller.result())
    pid = poller.result().person_id

    poller = dpg_operations.begin_create_group(gid, DynamicPersonGroup(name="my_dpg_name"))
    print(poller.result())

    result = dpg_operations.list_group()
    print(result)

    poller = dpg_operations.begin_update_group(gid, DynamicPersonGroup(name="my_dpg_name2", add_person_ids=[pid]))
    print(poller.result())

    result = dpg_operations.get_group(gid)
    print(result)

    result = dpg_operations.list_group_person(gid)
    print(result)

    result = person_operations.list_group_reference(pid)
    print(result)

    fids = [
        client.detect_from_url(
            url="https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/detection1.jpg",
            recognition_model=RecognitionModel.RECOGNITION_04,
        )[0].face_id
        for _ in range(3)
    ]

    result = dpg_operations.identify_from_dynamic_person_group(face_ids=fids, dynamic_person_group_id=gid)
    print(result)

    poller = dpg_operations.begin_delete_group(gid)
    print(poller.result())

    poller = person_operations.begin_delete_person(person_id=pid)
    print(poller.result())
