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
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Sequence,
    Tuple,
    Optional,
    Iterator,
)

from google.cloud.compute_v1.types import compute


class AggregatedListPager:
    """A pager for iterating through ``aggregated_list`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.compute_v1.types.UrlMapsAggregatedList` object, and
    provides an ``__iter__`` method to iterate through its
    ``items`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``AggregatedList`` requests and continue to iterate
    through the ``items`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.compute_v1.types.UrlMapsAggregatedList`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., compute.UrlMapsAggregatedList],
        request: compute.AggregatedListUrlMapsRequest,
        response: compute.UrlMapsAggregatedList,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.compute_v1.types.AggregatedListUrlMapsRequest):
                The initial request object.
            response (google.cloud.compute_v1.types.UrlMapsAggregatedList):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = compute.AggregatedListUrlMapsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[compute.UrlMapsAggregatedList]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[Tuple[str, compute.UrlMapsScopedList]]:
        for page in self.pages:
            yield from page.items.items()

    def get(self, key: str) -> Optional[compute.UrlMapsScopedList]:
        return self._response.items.get(key)

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListPager:
    """A pager for iterating through ``list`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.compute_v1.types.UrlMapList` object, and
    provides an ``__iter__`` method to iterate through its
    ``items`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``List`` requests and continue to iterate
    through the ``items`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.compute_v1.types.UrlMapList`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., compute.UrlMapList],
        request: compute.ListUrlMapsRequest,
        response: compute.UrlMapList,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.compute_v1.types.ListUrlMapsRequest):
                The initial request object.
            response (google.cloud.compute_v1.types.UrlMapList):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = compute.ListUrlMapsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[compute.UrlMapList]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[compute.UrlMap]:
        for page in self.pages:
            yield from page.items

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
