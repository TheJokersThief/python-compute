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
from google.cloud.compute_v1.services.disks import DisksClient
from google.cloud.compute_v1.services.disks import pagers
from google.cloud.compute_v1.services.disks import transports
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

    assert DisksClient._get_default_mtls_endpoint(None) is None
    assert DisksClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        DisksClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    )
    assert (
        DisksClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DisksClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert DisksClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [DisksClient,])
def test_disks_client_from_service_account_info(client_class):
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
    "transport_class,transport_name", [(transports.DisksRestTransport, "rest"),]
)
def test_disks_client_service_account_always_use_jwt(transport_class, transport_name):
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


@pytest.mark.parametrize("client_class", [DisksClient,])
def test_disks_client_from_service_account_file(client_class):
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


def test_disks_client_get_transport_class():
    transport = DisksClient.get_transport_class()
    available_transports = [
        transports.DisksRestTransport,
    ]
    assert transport in available_transports

    transport = DisksClient.get_transport_class("rest")
    assert transport == transports.DisksRestTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [(DisksClient, transports.DisksRestTransport, "rest"),],
)
@mock.patch.object(
    DisksClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DisksClient)
)
def test_disks_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(DisksClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(DisksClient, "get_transport_class") as gtc:
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
        (DisksClient, transports.DisksRestTransport, "rest", "true"),
        (DisksClient, transports.DisksRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    DisksClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DisksClient)
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_disks_client_mtls_env_auto(
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
    [(DisksClient, transports.DisksRestTransport, "rest"),],
)
def test_disks_client_client_options_scopes(
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
    [(DisksClient, transports.DisksRestTransport, "rest"),],
)
def test_disks_client_client_options_credentials_file(
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


def test_add_resource_policies_unary_rest(
    transport: str = "rest", request_type=compute.AddResourcePoliciesDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "disk": "sample3"}
    request_init[
        "disks_add_resource_policies_request_resource"
    ] = compute.DisksAddResourcePoliciesRequest(
        resource_policies=["resource_policies_value"]
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
        response = client.add_resource_policies_unary(request)

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


def test_add_resource_policies_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.AddResourcePoliciesDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "disk": "sample3"}
    request_init[
        "disks_add_resource_policies_request_resource"
    ] = compute.DisksAddResourcePoliciesRequest(
        resource_policies=["resource_policies_value"]
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
        client.add_resource_policies_unary(request)


def test_add_resource_policies_unary_rest_from_dict():
    test_add_resource_policies_unary_rest(request_type=dict)


def test_add_resource_policies_unary_rest_flattened(transport: str = "rest"):
    client = DisksClient(
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
        sample_request = {"project": "sample1", "zone": "sample2", "disk": "sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            disk="disk_value",
            disks_add_resource_policies_request_resource=compute.DisksAddResourcePoliciesRequest(
                resource_policies=["resource_policies_value"]
            ),
        )
        mock_args.update(sample_request)
        client.add_resource_policies_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/disks/{disk}/addResourcePolicies"
            % client.transport._host,
            args[1],
        )


def test_add_resource_policies_unary_rest_flattened_error(transport: str = "rest"):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.add_resource_policies_unary(
            compute.AddResourcePoliciesDiskRequest(),
            project="project_value",
            zone="zone_value",
            disk="disk_value",
            disks_add_resource_policies_request_resource=compute.DisksAddResourcePoliciesRequest(
                resource_policies=["resource_policies_value"]
            ),
        )


def test_aggregated_list_rest(
    transport: str = "rest", request_type=compute.AggregatedListDisksRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.DiskAggregatedList(
            id="id_value",
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
            unreachables=["unreachables_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.DiskAggregatedList.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.aggregated_list(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.AggregatedListPager)
    assert response.id == "id_value"
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"
    assert response.unreachables == ["unreachables_value"]


def test_aggregated_list_rest_bad_request(
    transport: str = "rest", request_type=compute.AggregatedListDisksRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
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
        client.aggregated_list(request)


def test_aggregated_list_rest_from_dict():
    test_aggregated_list_rest(request_type=dict)


def test_aggregated_list_rest_flattened(transport: str = "rest"):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.DiskAggregatedList()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.DiskAggregatedList.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(project="project_value",)
        mock_args.update(sample_request)
        client.aggregated_list(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/aggregated/disks"
            % client.transport._host,
            args[1],
        )


def test_aggregated_list_rest_flattened_error(transport: str = "rest"):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.aggregated_list(
            compute.AggregatedListDisksRequest(), project="project_value",
        )


def test_aggregated_list_rest_pager():
    client = DisksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.DiskAggregatedList(
                items={
                    "a": compute.DisksScopedList(),
                    "b": compute.DisksScopedList(),
                    "c": compute.DisksScopedList(),
                },
                next_page_token="abc",
            ),
            compute.DiskAggregatedList(items={}, next_page_token="def",),
            compute.DiskAggregatedList(
                items={"g": compute.DisksScopedList(),}, next_page_token="ghi",
            ),
            compute.DiskAggregatedList(
                items={"h": compute.DisksScopedList(), "i": compute.DisksScopedList(),},
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(compute.DiskAggregatedList.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"project": "sample1"}

        pager = client.aggregated_list(request=sample_request)

        assert isinstance(pager.get("a"), compute.DisksScopedList)
        assert pager.get("h") is None

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tuple) for i in results)
        for result in results:
            assert isinstance(result, tuple)
            assert tuple(type(t) for t in result) == (str, compute.DisksScopedList)

        assert pager.get("a") is None
        assert isinstance(pager.get("h"), compute.DisksScopedList)

        pages = list(client.aggregated_list(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_snapshot_unary_rest(
    transport: str = "rest", request_type=compute.CreateSnapshotDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "disk": "sample3"}
    request_init["snapshot_resource"] = compute.Snapshot(auto_created=True)
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
        response = client.create_snapshot_unary(request)

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


def test_create_snapshot_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.CreateSnapshotDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "disk": "sample3"}
    request_init["snapshot_resource"] = compute.Snapshot(auto_created=True)
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
        client.create_snapshot_unary(request)


def test_create_snapshot_unary_rest_from_dict():
    test_create_snapshot_unary_rest(request_type=dict)


def test_create_snapshot_unary_rest_flattened(transport: str = "rest"):
    client = DisksClient(
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
        sample_request = {"project": "sample1", "zone": "sample2", "disk": "sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            disk="disk_value",
            snapshot_resource=compute.Snapshot(auto_created=True),
        )
        mock_args.update(sample_request)
        client.create_snapshot_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/disks/{disk}/createSnapshot"
            % client.transport._host,
            args[1],
        )


def test_create_snapshot_unary_rest_flattened_error(transport: str = "rest"):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_snapshot_unary(
            compute.CreateSnapshotDiskRequest(),
            project="project_value",
            zone="zone_value",
            disk="disk_value",
            snapshot_resource=compute.Snapshot(auto_created=True),
        )


def test_delete_unary_rest(
    transport: str = "rest", request_type=compute.DeleteDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "disk": "sample3"}
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
    transport: str = "rest", request_type=compute.DeleteDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "disk": "sample3"}
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
    client = DisksClient(
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
        sample_request = {"project": "sample1", "zone": "sample2", "disk": "sample3"}

        # get truthy value for each flattened field
        mock_args = dict(project="project_value", zone="zone_value", disk="disk_value",)
        mock_args.update(sample_request)
        client.delete_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/disks/{disk}"
            % client.transport._host,
            args[1],
        )


def test_delete_unary_rest_flattened_error(transport: str = "rest"):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_unary(
            compute.DeleteDiskRequest(),
            project="project_value",
            zone="zone_value",
            disk="disk_value",
        )


def test_get_rest(transport: str = "rest", request_type=compute.GetDiskRequest):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "disk": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Disk(
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            id=205,
            kind="kind_value",
            label_fingerprint="label_fingerprint_value",
            last_attach_timestamp="last_attach_timestamp_value",
            last_detach_timestamp="last_detach_timestamp_value",
            license_codes=[1360],
            licenses=["licenses_value"],
            location_hint="location_hint_value",
            name="name_value",
            options="options_value",
            physical_block_size_bytes=2663,
            provisioned_iops=1740,
            region="region_value",
            replica_zones=["replica_zones_value"],
            resource_policies=["resource_policies_value"],
            satisfies_pzs=True,
            self_link="self_link_value",
            size_gb=739,
            source_disk="source_disk_value",
            source_disk_id="source_disk_id_value",
            source_image="source_image_value",
            source_image_id="source_image_id_value",
            source_snapshot="source_snapshot_value",
            source_snapshot_id="source_snapshot_id_value",
            source_storage_object="source_storage_object_value",
            status="status_value",
            type_="type__value",
            users=["users_value"],
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Disk.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Disk)
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.id == 205
    assert response.kind == "kind_value"
    assert response.label_fingerprint == "label_fingerprint_value"
    assert response.last_attach_timestamp == "last_attach_timestamp_value"
    assert response.last_detach_timestamp == "last_detach_timestamp_value"
    assert response.license_codes == [1360]
    assert response.licenses == ["licenses_value"]
    assert response.location_hint == "location_hint_value"
    assert response.name == "name_value"
    assert response.options == "options_value"
    assert response.physical_block_size_bytes == 2663
    assert response.provisioned_iops == 1740
    assert response.region == "region_value"
    assert response.replica_zones == ["replica_zones_value"]
    assert response.resource_policies == ["resource_policies_value"]
    assert response.satisfies_pzs is True
    assert response.self_link == "self_link_value"
    assert response.size_gb == 739
    assert response.source_disk == "source_disk_value"
    assert response.source_disk_id == "source_disk_id_value"
    assert response.source_image == "source_image_value"
    assert response.source_image_id == "source_image_id_value"
    assert response.source_snapshot == "source_snapshot_value"
    assert response.source_snapshot_id == "source_snapshot_id_value"
    assert response.source_storage_object == "source_storage_object_value"
    assert response.status == "status_value"
    assert response.type_ == "type__value"
    assert response.users == ["users_value"]
    assert response.zone == "zone_value"


def test_get_rest_bad_request(
    transport: str = "rest", request_type=compute.GetDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "disk": "sample3"}
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
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Disk()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Disk.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "zone": "sample2", "disk": "sample3"}

        # get truthy value for each flattened field
        mock_args = dict(project="project_value", zone="zone_value", disk="disk_value",)
        mock_args.update(sample_request)
        client.get(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/disks/{disk}"
            % client.transport._host,
            args[1],
        )


def test_get_rest_flattened_error(transport: str = "rest"):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get(
            compute.GetDiskRequest(),
            project="project_value",
            zone="zone_value",
            disk="disk_value",
        )


def test_get_iam_policy_rest(
    transport: str = "rest", request_type=compute.GetIamPolicyDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
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
    transport: str = "rest", request_type=compute.GetIamPolicyDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
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
    client = DisksClient(
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
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "resource": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", zone="zone_value", resource="resource_value",
        )
        mock_args.update(sample_request)
        client.get_iam_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/disks/{resource}/getIamPolicy"
            % client.transport._host,
            args[1],
        )


def test_get_iam_policy_rest_flattened_error(transport: str = "rest"):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_iam_policy(
            compute.GetIamPolicyDiskRequest(),
            project="project_value",
            zone="zone_value",
            resource="resource_value",
        )


def test_insert_unary_rest(
    transport: str = "rest", request_type=compute.InsertDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
    request_init["disk_resource"] = compute.Disk(
        creation_timestamp="creation_timestamp_value"
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
    transport: str = "rest", request_type=compute.InsertDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
    request_init["disk_resource"] = compute.Disk(
        creation_timestamp="creation_timestamp_value"
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
    client = DisksClient(
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
        sample_request = {"project": "sample1", "zone": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            disk_resource=compute.Disk(creation_timestamp="creation_timestamp_value"),
        )
        mock_args.update(sample_request)
        client.insert_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/disks"
            % client.transport._host,
            args[1],
        )


def test_insert_unary_rest_flattened_error(transport: str = "rest"):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.insert_unary(
            compute.InsertDiskRequest(),
            project="project_value",
            zone="zone_value",
            disk_resource=compute.Disk(creation_timestamp="creation_timestamp_value"),
        )


def test_list_rest(transport: str = "rest", request_type=compute.ListDisksRequest):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.DiskList(
            id="id_value",
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.DiskList.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPager)
    assert response.id == "id_value"
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"


def test_list_rest_bad_request(
    transport: str = "rest", request_type=compute.ListDisksRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
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


def test_list_rest_flattened(transport: str = "rest"):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.DiskList()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.DiskList.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "zone": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(project="project_value", zone="zone_value",)
        mock_args.update(sample_request)
        client.list(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/disks"
            % client.transport._host,
            args[1],
        )


def test_list_rest_flattened_error(transport: str = "rest"):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list(
            compute.ListDisksRequest(), project="project_value", zone="zone_value",
        )


def test_list_rest_pager():
    client = DisksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.DiskList(
                items=[compute.Disk(), compute.Disk(), compute.Disk(),],
                next_page_token="abc",
            ),
            compute.DiskList(items=[], next_page_token="def",),
            compute.DiskList(items=[compute.Disk(),], next_page_token="ghi",),
            compute.DiskList(items=[compute.Disk(), compute.Disk(),],),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(compute.DiskList.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"project": "sample1", "zone": "sample2"}

        pager = client.list(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.Disk) for i in results)

        pages = list(client.list(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_remove_resource_policies_unary_rest(
    transport: str = "rest", request_type=compute.RemoveResourcePoliciesDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "disk": "sample3"}
    request_init[
        "disks_remove_resource_policies_request_resource"
    ] = compute.DisksRemoveResourcePoliciesRequest(
        resource_policies=["resource_policies_value"]
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
        response = client.remove_resource_policies_unary(request)

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


def test_remove_resource_policies_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.RemoveResourcePoliciesDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "disk": "sample3"}
    request_init[
        "disks_remove_resource_policies_request_resource"
    ] = compute.DisksRemoveResourcePoliciesRequest(
        resource_policies=["resource_policies_value"]
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
        client.remove_resource_policies_unary(request)


def test_remove_resource_policies_unary_rest_from_dict():
    test_remove_resource_policies_unary_rest(request_type=dict)


def test_remove_resource_policies_unary_rest_flattened(transport: str = "rest"):
    client = DisksClient(
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
        sample_request = {"project": "sample1", "zone": "sample2", "disk": "sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            disk="disk_value",
            disks_remove_resource_policies_request_resource=compute.DisksRemoveResourcePoliciesRequest(
                resource_policies=["resource_policies_value"]
            ),
        )
        mock_args.update(sample_request)
        client.remove_resource_policies_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/disks/{disk}/removeResourcePolicies"
            % client.transport._host,
            args[1],
        )


def test_remove_resource_policies_unary_rest_flattened_error(transport: str = "rest"):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.remove_resource_policies_unary(
            compute.RemoveResourcePoliciesDiskRequest(),
            project="project_value",
            zone="zone_value",
            disk="disk_value",
            disks_remove_resource_policies_request_resource=compute.DisksRemoveResourcePoliciesRequest(
                resource_policies=["resource_policies_value"]
            ),
        )


def test_resize_unary_rest(
    transport: str = "rest", request_type=compute.ResizeDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "disk": "sample3"}
    request_init["disks_resize_request_resource"] = compute.DisksResizeRequest(
        size_gb=739
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
        response = client.resize_unary(request)

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


def test_resize_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.ResizeDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "disk": "sample3"}
    request_init["disks_resize_request_resource"] = compute.DisksResizeRequest(
        size_gb=739
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
        client.resize_unary(request)


def test_resize_unary_rest_from_dict():
    test_resize_unary_rest(request_type=dict)


def test_resize_unary_rest_flattened(transport: str = "rest"):
    client = DisksClient(
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
        sample_request = {"project": "sample1", "zone": "sample2", "disk": "sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            disk="disk_value",
            disks_resize_request_resource=compute.DisksResizeRequest(size_gb=739),
        )
        mock_args.update(sample_request)
        client.resize_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/disks/{disk}/resize"
            % client.transport._host,
            args[1],
        )


def test_resize_unary_rest_flattened_error(transport: str = "rest"):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.resize_unary(
            compute.ResizeDiskRequest(),
            project="project_value",
            zone="zone_value",
            disk="disk_value",
            disks_resize_request_resource=compute.DisksResizeRequest(size_gb=739),
        )


def test_set_iam_policy_rest(
    transport: str = "rest", request_type=compute.SetIamPolicyDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
    request_init["zone_set_policy_request_resource"] = compute.ZoneSetPolicyRequest(
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
    transport: str = "rest", request_type=compute.SetIamPolicyDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
    request_init["zone_set_policy_request_resource"] = compute.ZoneSetPolicyRequest(
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
    client = DisksClient(
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
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "resource": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            resource="resource_value",
            zone_set_policy_request_resource=compute.ZoneSetPolicyRequest(
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
            "https://%s/compute/v1/projects/{project}/zones/{zone}/disks/{resource}/setIamPolicy"
            % client.transport._host,
            args[1],
        )


def test_set_iam_policy_rest_flattened_error(transport: str = "rest"):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_iam_policy(
            compute.SetIamPolicyDiskRequest(),
            project="project_value",
            zone="zone_value",
            resource="resource_value",
            zone_set_policy_request_resource=compute.ZoneSetPolicyRequest(
                bindings=[compute.Binding(binding_id="binding_id_value")]
            ),
        )


def test_set_labels_unary_rest(
    transport: str = "rest", request_type=compute.SetLabelsDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
    request_init["zone_set_labels_request_resource"] = compute.ZoneSetLabelsRequest(
        label_fingerprint="label_fingerprint_value"
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
        response = client.set_labels_unary(request)

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


def test_set_labels_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.SetLabelsDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
    request_init["zone_set_labels_request_resource"] = compute.ZoneSetLabelsRequest(
        label_fingerprint="label_fingerprint_value"
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
        client.set_labels_unary(request)


def test_set_labels_unary_rest_from_dict():
    test_set_labels_unary_rest(request_type=dict)


def test_set_labels_unary_rest_flattened(transport: str = "rest"):
    client = DisksClient(
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
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "resource": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            resource="resource_value",
            zone_set_labels_request_resource=compute.ZoneSetLabelsRequest(
                label_fingerprint="label_fingerprint_value"
            ),
        )
        mock_args.update(sample_request)
        client.set_labels_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/disks/{resource}/setLabels"
            % client.transport._host,
            args[1],
        )


def test_set_labels_unary_rest_flattened_error(transport: str = "rest"):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_labels_unary(
            compute.SetLabelsDiskRequest(),
            project="project_value",
            zone="zone_value",
            resource="resource_value",
            zone_set_labels_request_resource=compute.ZoneSetLabelsRequest(
                label_fingerprint="label_fingerprint_value"
            ),
        )


def test_test_iam_permissions_rest(
    transport: str = "rest", request_type=compute.TestIamPermissionsDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
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
    transport: str = "rest", request_type=compute.TestIamPermissionsDiskRequest
):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
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
    client = DisksClient(
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
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "resource": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
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
            "https://%s/compute/v1/projects/{project}/zones/{zone}/disks/{resource}/testIamPermissions"
            % client.transport._host,
            args[1],
        )


def test_test_iam_permissions_rest_flattened_error(transport: str = "rest"):
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.test_iam_permissions(
            compute.TestIamPermissionsDiskRequest(),
            project="project_value",
            zone="zone_value",
            resource="resource_value",
            test_permissions_request_resource=compute.TestPermissionsRequest(
                permissions=["permissions_value"]
            ),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DisksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DisksClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DisksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DisksClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DisksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DisksClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DisksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = DisksClient(transport=transport)
    assert client.transport is transport


@pytest.mark.parametrize("transport_class", [transports.DisksRestTransport,])
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_disks_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.DisksTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_disks_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.compute_v1.services.disks.transports.DisksTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DisksTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "add_resource_policies",
        "aggregated_list",
        "create_snapshot",
        "delete",
        "get",
        "get_iam_policy",
        "insert",
        "list",
        "remove_resource_policies",
        "resize",
        "set_iam_policy",
        "set_labels",
        "test_iam_permissions",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()


def test_disks_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.compute_v1.services.disks.transports.DisksTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DisksTransport(
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


def test_disks_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.compute_v1.services.disks.transports.DisksTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DisksTransport()
        adc.assert_called_once()


def test_disks_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        DisksClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


def test_disks_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.DisksRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_disks_host_no_port():
    client = DisksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com"
        ),
    )
    assert client.transport._host == "compute.googleapis.com:443"


def test_disks_host_with_port():
    client = DisksClient(
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
    actual = DisksClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = DisksClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = DisksClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(folder=folder,)
    actual = DisksClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = DisksClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = DisksClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = DisksClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = DisksClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = DisksClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(project=project,)
    actual = DisksClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = DisksClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = DisksClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = DisksClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = DisksClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = DisksClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(transports.DisksTransport, "_prep_wrapped_messages") as prep:
        client = DisksClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(transports.DisksTransport, "_prep_wrapped_messages") as prep:
        transport_class = DisksClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close():
    transports = {
        "rest": "_session",
    }

    for transport, close_name in transports.items():
        client = DisksClient(
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
        client = DisksClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()
