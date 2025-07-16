"""Tests for templatetags"""

# pylint: disable=missing-docstring

from unittest import TestCase

from django.template.context import Context
from unittest_fixtures import Fixtures, given

from gbp_feeds.django.gbp_feeds.templatetags import url_tags

from . import lib


@given(lib.request)
class FullURLTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        context = Context({"request": fixtures.request})

        url = url_tags.full_url(context, "dashboard")

        self.assertEqual("http://testserver/", url)

    def test_with_kwargs(self, fixtures: Fixtures) -> None:
        context = Context({"request": fixtures.request})

        url = url_tags.full_url(context, "gbp-machines", machine="babette")

        self.assertEqual("http://testserver/machines/babette/", url)
