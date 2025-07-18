"""Tests for .views.utils"""

# pylint: disable=missing-docstring,unused-argument

from unittest import TestCase

import feedgenerator as fg
from unittest_fixtures import Fixtures, given, where

from gbp_feeds.django.gbp_feeds.views import utils

from . import lib


@given(lib.request, lib.pulled_builds)
class BuildFeedTests(TestCase):
    def test_rss(self, fixtures: Fixtures) -> None:
        builds = fixtures.publisher.repo.build_records.for_machine("babette")
        request = fixtures.request

        feed = utils.build_feed(builds, utils.FeedType.RSS, request)

        self.assertIsInstance(feed, fg.Rss201rev2Feed)
        self.assertEqual(3, feed.num_items())
        self.assertEqual("Gentoo Build Publisher", feed.feed["title"])
        self.assertEqual("http://testserver/", feed.feed["link"])
        self.assertEqual(
            "Latest Gentoo Build Publisher builds", feed.feed["description"]
        )

    def test_atom(self, fixtures: Fixtures) -> None:
        builds = fixtures.publisher.repo.build_records.for_machine("babette")
        request = fixtures.request

        feed = utils.build_feed(builds, utils.FeedType.ATOM, request)

        self.assertIsInstance(feed, fg.Atom1Feed)
        self.assertEqual(3, feed.num_items())
        self.assertEqual("Gentoo Build Publisher", feed.feed["title"])
        self.assertEqual("http://testserver/", feed.feed["link"])
        self.assertEqual(
            "Latest Gentoo Build Publisher builds", feed.feed["description"]
        )

    def test_item(self, fixtures: Fixtures) -> None:
        builds = fixtures.publisher.repo.build_records.for_machine("babette")
        request = fixtures.request

        feed = utils.build_feed(builds, utils.FeedType.ATOM, request)
        item = feed.items[0]

        self.assertEqual(item["title"], "GBP build: babette 2")
        self.assertEqual(item["link"], "http://testserver/machines/babette/builds/2/")
        self.assertEqual(item["description"], "Build babette.2 has been pulled")
        self.assertEqual(item["unique_id"], "babette.2")
        self.assertEqual(item["author_name"], "Gentoo Build Publisher")
        self.assertEqual(item["pubdate"], builds[0].completed)

    def test_item_note(self, fixtures: Fixtures) -> None:
        publisher = fixtures.publisher
        builds = publisher.repo.build_records.for_machine("babette")
        request = fixtures.request
        build = builds[0]
        build = builds[0] = publisher.repo.build_records.save(
            build, note="This is a note."
        )

        feed = utils.build_feed(builds, utils.FeedType.ATOM, request)
        item = feed.items[0]

        self.assertTrue(
            "This is a note." in item["content"], "Build note not found in feed content"
        )

    def test_item_published(self, fixtures: Fixtures) -> None:
        publisher = fixtures.publisher
        builds = publisher.repo.build_records.for_machine("babette")
        build = builds[0]
        publisher.publish(build)
        build = builds[0] = publisher.repo.build_records.get(build)

        feed = utils.build_feed(builds, utils.FeedType.ATOM, fixtures.request)
        item = feed.items[0]

        self.assertRegex(
            item["content"],
            r">Published</th>\W*<td>yes</td>",
            "Build not shown as published",
        )


@given(lib.request, lib.pulled_builds)
@where(pulled_builds__machines=["babette"], pulled_builds__num_builds=1)
class GetItemContentTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        build = fixtures.publisher.repo.build_records.for_machine("babette")[0]
        request = fixtures.request

        content = utils.get_item_content(build, request)

        self.assertTrue(content.startswith("<h3>babette 0</h3>"))


@given(lib.pulled_builds)
class GetCompletedBuilds(TestCase):
    def test_without_machine(self, fixtures: Fixtures) -> None:
        builds = utils.get_completed_builds(None)

        self.assertEqual(6, len(builds))

        prev = builds[0]
        for build in builds[1:]:
            self.assertGreater(prev.completed, build.completed)
            prev = build

    def test_with_machine(self, fixtures: Fixtures) -> None:
        machine = "babette"

        builds = utils.get_completed_builds(machine)

        self.assertEqual(3, len(builds))

        for build in builds:
            self.assertEqual(machine, build.machine)

    def test_with_noncomplete_build(self, fixtures: Fixtures) -> None:
        machine = "babette"
        publisher = fixtures.publisher
        repo = publisher.repo
        records = repo.build_records
        build = records.for_machine(machine)[0]

        # When the first (babette) build is not completed
        records.save(build, completed=None)

        builds = utils.get_completed_builds(machine)

        self.assertEqual(2, len(builds))
        self.assertNotIn(build, builds)


@given(lib.request)
class GetFeedTypeTests(TestCase):
    def test_atom(self, fixtures: Fixtures) -> None:
        request = fixtures.request
        request.path = "/feed.atom"

        feed_type = utils.get_feed_type(request)

        self.assertEqual(utils.FeedType.ATOM, feed_type)

    def test_rss(self, fixtures: Fixtures) -> None:
        request = fixtures.request
        request.path = "/feed.rss"

        feed_type = utils.get_feed_type(request)

        self.assertEqual(utils.FeedType.RSS, feed_type)

    def test_other(self, fixtures: Fixtures) -> None:
        request = fixtures.request
        request.path = "/index.html"

        with self.assertRaises(ValueError):
            utils.get_feed_type(request)


@given(lib.request, lib.pulled_builds)
@where(pulled_builds__machines=["babette"], pulled_builds__num_builds=1)
class BuildLinkTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        build = fixtures.publisher.repo.build_records.for_machine("babette")[0]
        request = fixtures.request

        url = utils.build_link(build, request)

        self.assertEqual("http://testserver/machines/babette/builds/0/", url)
