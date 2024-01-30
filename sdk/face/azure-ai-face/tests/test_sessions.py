# coding: utf-8
# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from azure.ai.face import FaceClient
from azure.ai.face.models import LivenessSessionCreationContent
from azure.core.credentials import AzureKeyCredential
from devtools_testutils import recorded_by_proxy
from test_case import FaceTest, FacePreparer


class TestSessions(FaceTest):
    def _create_session_client(self, **kwargs):
        endpoint = kwargs.pop("face_endpoint")
        key = kwargs.pop("face_key")
        face_client = self.create_client_from_credential(
            FaceClient, credential=AzureKeyCredential(key), endpoint=endpoint
        )
        return face_client.sessions

    @FacePreparer()
    @recorded_by_proxy
    def test_create_get_delete_liveness_session(self, **kwargs):
        client = self._create_session_client(**kwargs)
        content = self._build_liveness_session_creation_content()
        result = client.create_liveness_session(content)
        self._validate_session_creation_result(result)

        session_id = result.session_id
        print(session_id)
        session = client.get_liveness_session(session_id)
        self._validate_new_session_get_result(session, session_id)

        client.delete_liveness_session(session_id)

    @FacePreparer()
    @recorded_by_proxy
    def test_create_get_delete_liveness_with_verify_session_form_data(self, **kwargs):
        client = self._create_session_client(**kwargs)
        content = self._build_liveness_session_with_verify_creation_content()
        result = client.create_liveness_with_verify_session_by_form_data(content)
        self._validate_session_creation_result(result)

        session_id = result.session_id
        print(session_id)
        session = client.get_liveness_with_verify_session(session_id)
        self._validate_new_session_get_result(session, session_id)

        client.delete_liveness_with_verify_session(session_id)

    @FacePreparer()
    @recorded_by_proxy
    def test_create_delete_liveness_with_verify_session_json(self, **kwargs):
        client = self._create_session_client(**kwargs)
        content = self._build_liveness_session_creation_content()
        result = client.create_liveness_with_verify_session_by_json(content)
        self._validate_session_creation_result(result)

        client.delete_liveness_with_verify_session(result.session_id)

    @FacePreparer()
    @recorded_by_proxy
    def test_create_liveness_session_without_device_corelation(self, **kwargs):
        client = self._create_session_client(**kwargs)
        content = LivenessSessionCreationContent(
            device_correlation_id="",
            liveness_operation_mode=self.TEST_LIVENESS_OPERATION_MODE,
            device_correlation_id_set_in_client=False,
        )
        result = client.create_liveness_session(content)
        self._validate_session_creation_result(result)

        client.delete_liveness_session(result.session_id)

    @FacePreparer()
    @recorded_by_proxy
    def test_get_liveness_session_audit_entries(self, **kwargs):
        session_id = "3b8b94dc-c398-4dc5-85ae-f7d721648d18"
        number_of_entries = 3
        top_limit = 1

        client = self._create_session_client(**kwargs)
        entry_list = client.list_liveness_session_audit_entries(session_id)
        assert len(entry_list) == number_of_entries

        for entry in entry_list:
            self._validate_liveness_session_audit_entry(entry, session_id)

        entry_list_with_query = client.list_liveness_session_audit_entries(
            session_id, start=entry_list[0].id, top=top_limit
        )
        assert len(entry_list_with_query) == top_limit
        assert entry_list_with_query[0].id == entry_list[1].id

    @FacePreparer()
    @recorded_by_proxy
    def test_get_liveness_sessions(self, **kwargs):
        number_of_sessions = 3
        client = self._create_session_client(**kwargs)
        session_ids = []

        try:
            content = self._build_liveness_session_creation_content()
            for i in range(number_of_sessions):
                result = client.create_liveness_session(content)
                session_ids.append(result.session_id)

            session_list = client.list_liveness_sessions()
            for session in session_list:
                self._validate_liveness_session_item(session)
        finally:
            for id in session_ids:
                client.delete_liveness_session(id)
