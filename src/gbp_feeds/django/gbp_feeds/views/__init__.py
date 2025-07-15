"""Django views for gbp-feeds"""

from django.http import HttpRequest, HttpResponse
from gentoo_build_publisher.django.gentoo_build_publisher.views.utils import view

from . import utils


@view("feed.rss")
@view("feed.atom")
@view("machines/<str:machine>/feed.rss")
@view("machines/<str:machine>/feed.atom")
def _(request: HttpRequest, *, machine: str | None = None) -> HttpResponse:
    """View to return the feed for the given machine, if applicable"""
    feed_type = utils.get_feed_type(request)
    feed = utils.build_feed(utils.get_completed_builds(machine), feed_type, request)

    response = HttpResponse(feed.writeString("utf-8"), content_type=str(feed_type))

    return response
