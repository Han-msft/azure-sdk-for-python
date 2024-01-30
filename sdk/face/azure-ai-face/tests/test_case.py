# coding=utf-8
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import functools
from pathlib import Path

from azure.ai.face.models import SessionStatus, LivenessSessionCreationContent, LivenessWithVerifySessionCreationContent
from devtools_testutils import AzureRecordedTestCase, EnvironmentVariableLoader


class FaceTest(AzureRecordedTestCase):
    TEST_DEVICE_CORELATION_ID = "dummy-test-id"
    TEST_LIVENESS_OPERATION_MODE = "Passive"
    TEST_SAMPLE_IMAGE = "sample.jpg"

    def _build_liveness_session_creation_content(self):
        return LivenessSessionCreationContent(
            device_correlation_id=self.TEST_DEVICE_CORELATION_ID,
            liveness_operation_mode=self.TEST_LIVENESS_OPERATION_MODE,
        )

    def _build_liveness_session_with_verify_creation_content(self):
        sample_path = Path(__file__).resolve().parent / self.TEST_SAMPLE_IMAGE
        with open(sample_path, "rb") as fd:
            file = fd.read()
        return LivenessWithVerifySessionCreationContent(
            parameters=self._build_liveness_session_creation_content(), verify_image=file
        )

    def _validate_session_creation_result(self, result):
        assert result.session_id is not None
        assert result.auth_token is not None

    def _validate_new_session_get_result(self, session, id):
        assert session.id == id
        assert session.status == SessionStatus.NOT_STARTED
        assert session.device_correlation_id == self.TEST_DEVICE_CORELATION_ID
        assert session.auth_token_time_to_live_in_seconds == 600
        assert session.session_expired == False
        assert session.created_date_time is not None

    def _validate_liveness_session_audit_entry(self, entry, id):
        assert entry.session_id == id
        assert entry.id is not None
        assert entry.request_id is not None
        assert entry.client_request_id is not None
        assert entry.received_date_time is not None
        assert entry.digest is not None
        assert entry.request.url is not None
        assert entry.request.method is not None
        assert entry.request.content_type is not None
        assert entry.response.body is not None
        assert entry.response.status_code is not None
        assert entry.response.latency_in_milliseconds is not None

    def _validate_liveness_session_item(self, item):
        assert item.id is not None
        assert item.device_correlation_id is not None
        assert item.auth_token_time_to_live_in_seconds is not None
        assert item.session_expired is not None
        assert item.created_date_time is not None


FacePreparer = functools.partial(
    EnvironmentVariableLoader,
    "face",
    face_endpoint="https://face_resource.cognitiveservices.azure.com/",
    face_key="Sanitized_Face_Key",
)
