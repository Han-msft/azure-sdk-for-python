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
from azure.ai.face.models import LivenessSessionParameters, LivenessWithVerifySessionParameters
from dotenv import find_dotenv, load_dotenv

TEST_DEVICE_CORELATION_ID = "dummy-test-id"
TEST_LIVENESS_OPERATION_MODE = "Passive"

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    endpoint = os.environ["FACE_ENDPOINT"]
    key = os.environ["FACE_KEY"]

    client = FaceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    operations = client.liveness_with_verify_sessions

    parameters = LivenessSessionParameters(
        device_correlation_id=TEST_DEVICE_CORELATION_ID,
        liveness_operation_mode=TEST_LIVENESS_OPERATION_MODE,
    )

    creation_result = operations.create_session(parameters)
    print(f"Liveness session created with ID {creation_result.session_id}.")
    print(f"Token: {creation_result.auth_token}")

    operations.delete_session(creation_result.session_id)
    print(f"Liveness session {creation_result.session_id} deleted.")

    sample_path = Path(__file__).resolve().parent / "sample.jpg"
    with open(sample_path, "rb") as fd:
        file = fd.read()
    sessionWithVerify = LivenessWithVerifySessionParameters(parameters=parameters, verify_image=file)

    creation_result = operations.create_session_with_verify_image(sessionWithVerify)
    print(f"Liveness session created with ID {creation_result.session_id}.")
    print(f"Token: {creation_result.auth_token}")

    operations.delete_session(creation_result.session_id)
    print(f"Liveness session {creation_result.session_id} deleted.")
