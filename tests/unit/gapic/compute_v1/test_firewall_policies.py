# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from requests import Response
from requests import Request
from requests.sessions import Session

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.compute_v1.services.firewall_policies import FirewallPoliciesClient
from google.cloud.compute_v1.services.firewall_policies import pagers
from google.cloud.compute_v1.services.firewall_policies import transports
from google.cloud.compute_v1.types import compute
from google.oauth2 import service_account
import google.auth


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert FirewallPoliciesClient._get_default_mtls_endpoint(None) is None
    assert (
        FirewallPoliciesClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        FirewallPoliciesClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        FirewallPoliciesClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        FirewallPoliciesClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        FirewallPoliciesClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize("client_class", [FirewallPoliciesClient,])
def test_firewall_policies_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "compute.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [(transports.FirewallPoliciesRestTransport, "rest"),],
)
def test_firewall_policies_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize("client_class", [FirewallPoliciesClient,])
def test_firewall_policies_client_from_service_account_file(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "compute.googleapis.com:443"


def test_firewall_policies_client_get_transport_class():
    transport = FirewallPoliciesClient.get_transport_class()
    available_transports = [
        transports.FirewallPoliciesRestTransport,
    ]
    assert transport in available_transports

    transport = FirewallPoliciesClient.get_transport_class("rest")
    assert transport == transports.FirewallPoliciesRestTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [(FirewallPoliciesClient, transports.FirewallPoliciesRestTransport, "rest"),],
)
@mock.patch.object(
    FirewallPoliciesClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(FirewallPoliciesClient),
)
def test_firewall_policies_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(FirewallPoliciesClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(FirewallPoliciesClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            FirewallPoliciesClient,
            transports.FirewallPoliciesRestTransport,
            "rest",
            "true",
        ),
        (
            FirewallPoliciesClient,
            transports.FirewallPoliciesRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    FirewallPoliciesClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(FirewallPoliciesClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_firewall_policies_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name, client_options=options)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [(FirewallPoliciesClient, transports.FirewallPoliciesRestTransport, "rest"),],
)
def test_firewall_policies_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [(FirewallPoliciesClient, transports.FirewallPoliciesRestTransport, "rest"),],
)
def test_firewall_policies_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


def test_add_association_unary_rest(
    transport: str = "rest", request_type=compute.AddAssociationFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request_init[
        "firewall_policy_association_resource"
    ] = compute.FirewallPolicyAssociation(attachment_target="attachment_target_value")
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.add_association_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_add_association_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.AddAssociationFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request_init[
        "firewall_policy_association_resource"
    ] = compute.FirewallPolicyAssociation(attachment_target="attachment_target_value")
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.add_association_unary(request)


def test_add_association_unary_rest_from_dict():
    test_add_association_unary_rest(request_type=dict)


def test_add_association_unary_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"firewall_policy": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            firewall_policy="firewall_policy_value",
            firewall_policy_association_resource=compute.FirewallPolicyAssociation(
                attachment_target="attachment_target_value"
            ),
        )
        mock_args.update(sample_request)
        client.add_association_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies/{firewall_policy}/addAssociation"
            % client.transport._host,
            args[1],
        )


def test_add_association_unary_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.add_association_unary(
            compute.AddAssociationFirewallPolicyRequest(),
            firewall_policy="firewall_policy_value",
            firewall_policy_association_resource=compute.FirewallPolicyAssociation(
                attachment_target="attachment_target_value"
            ),
        )


def test_add_rule_unary_rest(
    transport: str = "rest", request_type=compute.AddRuleFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request_init["firewall_policy_rule_resource"] = compute.FirewallPolicyRule(
        action="action_value"
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.add_rule_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_add_rule_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.AddRuleFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request_init["firewall_policy_rule_resource"] = compute.FirewallPolicyRule(
        action="action_value"
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.add_rule_unary(request)


def test_add_rule_unary_rest_from_dict():
    test_add_rule_unary_rest(request_type=dict)


def test_add_rule_unary_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"firewall_policy": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            firewall_policy="firewall_policy_value",
            firewall_policy_rule_resource=compute.FirewallPolicyRule(
                action="action_value"
            ),
        )
        mock_args.update(sample_request)
        client.add_rule_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies/{firewall_policy}/addRule"
            % client.transport._host,
            args[1],
        )


def test_add_rule_unary_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.add_rule_unary(
            compute.AddRuleFirewallPolicyRequest(),
            firewall_policy="firewall_policy_value",
            firewall_policy_rule_resource=compute.FirewallPolicyRule(
                action="action_value"
            ),
        )


def test_clone_rules_unary_rest(
    transport: str = "rest", request_type=compute.CloneRulesFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.clone_rules_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_clone_rules_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.CloneRulesFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.clone_rules_unary(request)


def test_clone_rules_unary_rest_from_dict():
    test_clone_rules_unary_rest(request_type=dict)


def test_clone_rules_unary_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"firewall_policy": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(firewall_policy="firewall_policy_value",)
        mock_args.update(sample_request)
        client.clone_rules_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies/{firewall_policy}/cloneRules"
            % client.transport._host,
            args[1],
        )


def test_clone_rules_unary_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.clone_rules_unary(
            compute.CloneRulesFirewallPolicyRequest(),
            firewall_policy="firewall_policy_value",
        )


def test_delete_unary_rest(
    transport: str = "rest", request_type=compute.DeleteFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_delete_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.DeleteFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_unary(request)


def test_delete_unary_rest_from_dict():
    test_delete_unary_rest(request_type=dict)


def test_delete_unary_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"firewall_policy": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(firewall_policy="firewall_policy_value",)
        mock_args.update(sample_request)
        client.delete_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies/{firewall_policy}"
            % client.transport._host,
            args[1],
        )


def test_delete_unary_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_unary(
            compute.DeleteFirewallPolicyRequest(),
            firewall_policy="firewall_policy_value",
        )


def test_get_rest(
    transport: str = "rest", request_type=compute.GetFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.FirewallPolicy(
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            display_name="display_name_value",
            fingerprint="fingerprint_value",
            id=205,
            kind="kind_value",
            name="name_value",
            parent="parent_value",
            rule_tuple_count=1737,
            self_link="self_link_value",
            self_link_with_id="self_link_with_id_value",
            short_name="short_name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.FirewallPolicy.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.FirewallPolicy)
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.display_name == "display_name_value"
    assert response.fingerprint == "fingerprint_value"
    assert response.id == 205
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.rule_tuple_count == 1737
    assert response.self_link == "self_link_value"
    assert response.self_link_with_id == "self_link_with_id_value"
    assert response.short_name == "short_name_value"


def test_get_rest_bad_request(
    transport: str = "rest", request_type=compute.GetFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get(request)


def test_get_rest_from_dict():
    test_get_rest(request_type=dict)


def test_get_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.FirewallPolicy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.FirewallPolicy.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"firewall_policy": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(firewall_policy="firewall_policy_value",)
        mock_args.update(sample_request)
        client.get(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies/{firewall_policy}"
            % client.transport._host,
            args[1],
        )


def test_get_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get(
            compute.GetFirewallPolicyRequest(), firewall_policy="firewall_policy_value",
        )


def test_get_association_rest(
    transport: str = "rest", request_type=compute.GetAssociationFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.FirewallPolicyAssociation(
            attachment_target="attachment_target_value",
            display_name="display_name_value",
            firewall_policy_id="firewall_policy_id_value",
            name="name_value",
            short_name="short_name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.FirewallPolicyAssociation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_association(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.FirewallPolicyAssociation)
    assert response.attachment_target == "attachment_target_value"
    assert response.display_name == "display_name_value"
    assert response.firewall_policy_id == "firewall_policy_id_value"
    assert response.name == "name_value"
    assert response.short_name == "short_name_value"


def test_get_association_rest_bad_request(
    transport: str = "rest", request_type=compute.GetAssociationFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_association(request)


def test_get_association_rest_from_dict():
    test_get_association_rest(request_type=dict)


def test_get_association_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.FirewallPolicyAssociation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.FirewallPolicyAssociation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"firewall_policy": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(firewall_policy="firewall_policy_value",)
        mock_args.update(sample_request)
        client.get_association(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies/{firewall_policy}/getAssociation"
            % client.transport._host,
            args[1],
        )


def test_get_association_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_association(
            compute.GetAssociationFirewallPolicyRequest(),
            firewall_policy="firewall_policy_value",
        )


def test_get_iam_policy_rest(
    transport: str = "rest", request_type=compute.GetIamPolicyFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Policy(etag="etag_value", iam_owned=True, version=774,)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Policy.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Policy)
    assert response.etag == "etag_value"
    assert response.iam_owned is True
    assert response.version == 774


def test_get_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=compute.GetIamPolicyFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_iam_policy(request)


def test_get_iam_policy_rest_from_dict():
    test_get_iam_policy_rest(request_type=dict)


def test_get_iam_policy_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Policy.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"resource": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(resource="resource_value",)
        mock_args.update(sample_request)
        client.get_iam_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies/{resource}/getIamPolicy"
            % client.transport._host,
            args[1],
        )


def test_get_iam_policy_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_iam_policy(
            compute.GetIamPolicyFirewallPolicyRequest(), resource="resource_value",
        )


def test_get_rule_rest(
    transport: str = "rest", request_type=compute.GetRuleFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.FirewallPolicyRule(
            action="action_value",
            description="description_value",
            direction="direction_value",
            disabled=True,
            enable_logging=True,
            kind="kind_value",
            priority=898,
            rule_tuple_count=1737,
            target_resources=["target_resources_value"],
            target_service_accounts=["target_service_accounts_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.FirewallPolicyRule.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_rule(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.FirewallPolicyRule)
    assert response.action == "action_value"
    assert response.description == "description_value"
    assert response.direction == "direction_value"
    assert response.disabled is True
    assert response.enable_logging is True
    assert response.kind == "kind_value"
    assert response.priority == 898
    assert response.rule_tuple_count == 1737
    assert response.target_resources == ["target_resources_value"]
    assert response.target_service_accounts == ["target_service_accounts_value"]


def test_get_rule_rest_bad_request(
    transport: str = "rest", request_type=compute.GetRuleFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_rule(request)


def test_get_rule_rest_from_dict():
    test_get_rule_rest(request_type=dict)


def test_get_rule_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.FirewallPolicyRule()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.FirewallPolicyRule.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"firewall_policy": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(firewall_policy="firewall_policy_value",)
        mock_args.update(sample_request)
        client.get_rule(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies/{firewall_policy}/getRule"
            % client.transport._host,
            args[1],
        )


def test_get_rule_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_rule(
            compute.GetRuleFirewallPolicyRequest(),
            firewall_policy="firewall_policy_value",
        )


def test_insert_unary_rest(
    transport: str = "rest", request_type=compute.InsertFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {}
    request_init["firewall_policy_resource"] = compute.FirewallPolicy(
        associations=[
            compute.FirewallPolicyAssociation(
                attachment_target="attachment_target_value"
            )
        ]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.insert_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_insert_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.InsertFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {}
    request_init["firewall_policy_resource"] = compute.FirewallPolicy(
        associations=[
            compute.FirewallPolicyAssociation(
                attachment_target="attachment_target_value"
            )
        ]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.insert_unary(request)


def test_insert_unary_rest_from_dict():
    test_insert_unary_rest(request_type=dict)


def test_insert_unary_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {}

        # get truthy value for each flattened field
        mock_args = dict(
            parent_id="parent_id_value",
            firewall_policy_resource=compute.FirewallPolicy(
                associations=[
                    compute.FirewallPolicyAssociation(
                        attachment_target="attachment_target_value"
                    )
                ]
            ),
        )
        mock_args.update(sample_request)
        client.insert_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies"
            % client.transport._host,
            args[1],
        )


def test_insert_unary_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.insert_unary(
            compute.InsertFirewallPolicyRequest(),
            parent_id="parent_id_value",
            firewall_policy_resource=compute.FirewallPolicy(
                associations=[
                    compute.FirewallPolicyAssociation(
                        attachment_target="attachment_target_value"
                    )
                ]
            ),
        )


def test_list_rest(
    transport: str = "rest", request_type=compute.ListFirewallPoliciesRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.FirewallPolicyList(
            id="id_value", kind="kind_value", next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.FirewallPolicyList.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPager)
    assert response.id == "id_value"
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"


def test_list_rest_bad_request(
    transport: str = "rest", request_type=compute.ListFirewallPoliciesRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list(request)


def test_list_rest_from_dict():
    test_list_rest(request_type=dict)


def test_list_rest_pager():
    client = FirewallPoliciesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.FirewallPolicyList(
                items=[
                    compute.FirewallPolicy(),
                    compute.FirewallPolicy(),
                    compute.FirewallPolicy(),
                ],
                next_page_token="abc",
            ),
            compute.FirewallPolicyList(items=[], next_page_token="def",),
            compute.FirewallPolicyList(
                items=[compute.FirewallPolicy(),], next_page_token="ghi",
            ),
            compute.FirewallPolicyList(
                items=[compute.FirewallPolicy(), compute.FirewallPolicy(),],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(compute.FirewallPolicyList.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {}

        pager = client.list(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.FirewallPolicy) for i in results)

        pages = list(client.list(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_associations_rest(
    transport: str = "rest", request_type=compute.ListAssociationsFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.FirewallPoliciesListAssociationsResponse(
            kind="kind_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.FirewallPoliciesListAssociationsResponse.to_json(
            return_value
        )
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_associations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.FirewallPoliciesListAssociationsResponse)
    assert response.kind == "kind_value"


def test_list_associations_rest_bad_request(
    transport: str = "rest", request_type=compute.ListAssociationsFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_associations(request)


def test_list_associations_rest_from_dict():
    test_list_associations_rest(request_type=dict)


def test_move_unary_rest(
    transport: str = "rest", request_type=compute.MoveFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.move_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_move_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.MoveFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.move_unary(request)


def test_move_unary_rest_from_dict():
    test_move_unary_rest(request_type=dict)


def test_move_unary_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"firewall_policy": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            firewall_policy="firewall_policy_value", parent_id="parent_id_value",
        )
        mock_args.update(sample_request)
        client.move_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies/{firewall_policy}/move"
            % client.transport._host,
            args[1],
        )


def test_move_unary_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.move_unary(
            compute.MoveFirewallPolicyRequest(),
            firewall_policy="firewall_policy_value",
            parent_id="parent_id_value",
        )


def test_patch_unary_rest(
    transport: str = "rest", request_type=compute.PatchFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request_init["firewall_policy_resource"] = compute.FirewallPolicy(
        associations=[
            compute.FirewallPolicyAssociation(
                attachment_target="attachment_target_value"
            )
        ]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.patch_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_patch_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.PatchFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request_init["firewall_policy_resource"] = compute.FirewallPolicy(
        associations=[
            compute.FirewallPolicyAssociation(
                attachment_target="attachment_target_value"
            )
        ]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.patch_unary(request)


def test_patch_unary_rest_from_dict():
    test_patch_unary_rest(request_type=dict)


def test_patch_unary_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"firewall_policy": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            firewall_policy="firewall_policy_value",
            firewall_policy_resource=compute.FirewallPolicy(
                associations=[
                    compute.FirewallPolicyAssociation(
                        attachment_target="attachment_target_value"
                    )
                ]
            ),
        )
        mock_args.update(sample_request)
        client.patch_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies/{firewall_policy}"
            % client.transport._host,
            args[1],
        )


def test_patch_unary_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch_unary(
            compute.PatchFirewallPolicyRequest(),
            firewall_policy="firewall_policy_value",
            firewall_policy_resource=compute.FirewallPolicy(
                associations=[
                    compute.FirewallPolicyAssociation(
                        attachment_target="attachment_target_value"
                    )
                ]
            ),
        )


def test_patch_rule_unary_rest(
    transport: str = "rest", request_type=compute.PatchRuleFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request_init["firewall_policy_rule_resource"] = compute.FirewallPolicyRule(
        action="action_value"
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.patch_rule_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_patch_rule_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.PatchRuleFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request_init["firewall_policy_rule_resource"] = compute.FirewallPolicyRule(
        action="action_value"
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.patch_rule_unary(request)


def test_patch_rule_unary_rest_from_dict():
    test_patch_rule_unary_rest(request_type=dict)


def test_patch_rule_unary_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"firewall_policy": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            firewall_policy="firewall_policy_value",
            firewall_policy_rule_resource=compute.FirewallPolicyRule(
                action="action_value"
            ),
        )
        mock_args.update(sample_request)
        client.patch_rule_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies/{firewall_policy}/patchRule"
            % client.transport._host,
            args[1],
        )


def test_patch_rule_unary_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch_rule_unary(
            compute.PatchRuleFirewallPolicyRequest(),
            firewall_policy="firewall_policy_value",
            firewall_policy_rule_resource=compute.FirewallPolicyRule(
                action="action_value"
            ),
        )


def test_remove_association_unary_rest(
    transport: str = "rest", request_type=compute.RemoveAssociationFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.remove_association_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_remove_association_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.RemoveAssociationFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.remove_association_unary(request)


def test_remove_association_unary_rest_from_dict():
    test_remove_association_unary_rest(request_type=dict)


def test_remove_association_unary_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"firewall_policy": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(firewall_policy="firewall_policy_value",)
        mock_args.update(sample_request)
        client.remove_association_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies/{firewall_policy}/removeAssociation"
            % client.transport._host,
            args[1],
        )


def test_remove_association_unary_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.remove_association_unary(
            compute.RemoveAssociationFirewallPolicyRequest(),
            firewall_policy="firewall_policy_value",
        )


def test_remove_rule_unary_rest(
    transport: str = "rest", request_type=compute.RemoveRuleFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.remove_rule_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_remove_rule_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.RemoveRuleFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"firewall_policy": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.remove_rule_unary(request)


def test_remove_rule_unary_rest_from_dict():
    test_remove_rule_unary_rest(request_type=dict)


def test_remove_rule_unary_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"firewall_policy": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(firewall_policy="firewall_policy_value",)
        mock_args.update(sample_request)
        client.remove_rule_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies/{firewall_policy}/removeRule"
            % client.transport._host,
            args[1],
        )


def test_remove_rule_unary_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.remove_rule_unary(
            compute.RemoveRuleFirewallPolicyRequest(),
            firewall_policy="firewall_policy_value",
        )


def test_set_iam_policy_rest(
    transport: str = "rest", request_type=compute.SetIamPolicyFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "sample1"}
    request_init[
        "global_organization_set_policy_request_resource"
    ] = compute.GlobalOrganizationSetPolicyRequest(
        bindings=[compute.Binding(binding_id="binding_id_value")]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Policy(etag="etag_value", iam_owned=True, version=774,)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Policy.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Policy)
    assert response.etag == "etag_value"
    assert response.iam_owned is True
    assert response.version == 774


def test_set_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=compute.SetIamPolicyFirewallPolicyRequest
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "sample1"}
    request_init[
        "global_organization_set_policy_request_resource"
    ] = compute.GlobalOrganizationSetPolicyRequest(
        bindings=[compute.Binding(binding_id="binding_id_value")]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_iam_policy(request)


def test_set_iam_policy_rest_from_dict():
    test_set_iam_policy_rest(request_type=dict)


def test_set_iam_policy_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Policy.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"resource": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            resource="resource_value",
            global_organization_set_policy_request_resource=compute.GlobalOrganizationSetPolicyRequest(
                bindings=[compute.Binding(binding_id="binding_id_value")]
            ),
        )
        mock_args.update(sample_request)
        client.set_iam_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies/{resource}/setIamPolicy"
            % client.transport._host,
            args[1],
        )


def test_set_iam_policy_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_iam_policy(
            compute.SetIamPolicyFirewallPolicyRequest(),
            resource="resource_value",
            global_organization_set_policy_request_resource=compute.GlobalOrganizationSetPolicyRequest(
                bindings=[compute.Binding(binding_id="binding_id_value")]
            ),
        )


def test_test_iam_permissions_rest(
    transport: str = "rest",
    request_type=compute.TestIamPermissionsFirewallPolicyRequest,
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "sample1"}
    request_init["test_permissions_request_resource"] = compute.TestPermissionsRequest(
        permissions=["permissions_value"]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.TestPermissionsResponse(
            permissions=["permissions_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.TestPermissionsResponse.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.test_iam_permissions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.TestPermissionsResponse)
    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_rest_bad_request(
    transport: str = "rest",
    request_type=compute.TestIamPermissionsFirewallPolicyRequest,
):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "sample1"}
    request_init["test_permissions_request_resource"] = compute.TestPermissionsRequest(
        permissions=["permissions_value"]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.test_iam_permissions(request)


def test_test_iam_permissions_rest_from_dict():
    test_test_iam_permissions_rest(request_type=dict)


def test_test_iam_permissions_rest_flattened(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.TestPermissionsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.TestPermissionsResponse.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"resource": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            resource="resource_value",
            test_permissions_request_resource=compute.TestPermissionsRequest(
                permissions=["permissions_value"]
            ),
        )
        mock_args.update(sample_request)
        client.test_iam_permissions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/locations/global/firewallPolicies/{resource}/testIamPermissions"
            % client.transport._host,
            args[1],
        )


def test_test_iam_permissions_rest_flattened_error(transport: str = "rest"):
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.test_iam_permissions(
            compute.TestIamPermissionsFirewallPolicyRequest(),
            resource="resource_value",
            test_permissions_request_resource=compute.TestPermissionsRequest(
                permissions=["permissions_value"]
            ),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.FirewallPoliciesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = FirewallPoliciesClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.FirewallPoliciesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = FirewallPoliciesClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.FirewallPoliciesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = FirewallPoliciesClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.FirewallPoliciesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = FirewallPoliciesClient(transport=transport)
    assert client.transport is transport


@pytest.mark.parametrize("transport_class", [transports.FirewallPoliciesRestTransport,])
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_firewall_policies_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.FirewallPoliciesTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_firewall_policies_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.compute_v1.services.firewall_policies.transports.FirewallPoliciesTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.FirewallPoliciesTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "add_association",
        "add_rule",
        "clone_rules",
        "delete",
        "get",
        "get_association",
        "get_iam_policy",
        "get_rule",
        "insert",
        "list",
        "list_associations",
        "move",
        "patch",
        "patch_rule",
        "remove_association",
        "remove_rule",
        "set_iam_policy",
        "test_iam_permissions",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()


def test_firewall_policies_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.compute_v1.services.firewall_policies.transports.FirewallPoliciesTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.FirewallPoliciesTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_firewall_policies_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.compute_v1.services.firewall_policies.transports.FirewallPoliciesTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.FirewallPoliciesTransport()
        adc.assert_called_once()


def test_firewall_policies_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        FirewallPoliciesClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


def test_firewall_policies_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.FirewallPoliciesRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_firewall_policies_host_no_port():
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com"
        ),
    )
    assert client.transport._host == "compute.googleapis.com:443"


def test_firewall_policies_host_with_port():
    client = FirewallPoliciesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "compute.googleapis.com:8000"


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = FirewallPoliciesClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = FirewallPoliciesClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = FirewallPoliciesClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(folder=folder,)
    actual = FirewallPoliciesClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = FirewallPoliciesClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = FirewallPoliciesClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = FirewallPoliciesClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = FirewallPoliciesClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = FirewallPoliciesClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(project=project,)
    actual = FirewallPoliciesClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = FirewallPoliciesClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = FirewallPoliciesClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = FirewallPoliciesClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = FirewallPoliciesClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = FirewallPoliciesClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.FirewallPoliciesTransport, "_prep_wrapped_messages"
    ) as prep:
        client = FirewallPoliciesClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.FirewallPoliciesTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = FirewallPoliciesClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close():
    transports = {
        "rest": "_session",
    }

    for transport, close_name in transports.items():
        client = FirewallPoliciesClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
    ]
    for transport in transports:
        client = FirewallPoliciesClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()
