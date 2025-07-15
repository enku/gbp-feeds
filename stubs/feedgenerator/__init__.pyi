# pylint: disable=too-few-public-methods,missing-docstring,unused-argument
# pylint: disable=too-many-arguments,too-many-locals,too-many-positional-arguments
import datetime as dt
from typing import Any, Iterable

class SyndicationFeed:
    def __init__(
        self,
        title: str,
        link: str,
        description: str,
        language: str | None = None,
        author_email: str | None = None,
        author_name: str | None = None,
        author_link: str | None = None,
        subtitle: str | None = None,
        categories: Iterable[Any] | None = None,
        feed_url: str | None = None,
        feed_copyright: Any | None = None,
        feed_guid: str | None = None,
        ttl: Any | None = None,
        stylesheets: Iterable[str] | None = None,
        **kwargs: Any,
    ) -> None: ...
    def add_item(
        self,
        title: str,
        link: str,
        description: str,
        author_email: str | None = None,
        author_name: str | None = None,
        author_link: str | None = None,
        pubdate: dt.datetime | None = None,
        comments: str | None = None,
        unique_id: str | None = None,
        unique_id_is_permalink: bool | None = None,
        categories: Iterable[Any] = (),
        item_copyright: str | None = None,
        ttl: Any | None = None,
        updateddate: dt.datetime | None = None,
        enclosures: Any | None = None,
        **kwargs: Any,
    ) -> None: ...
    def writeString(self, encoding: str) -> str: ...

class Atom1Feed(SyndicationFeed): ...
class Rss201rev2Feed(SyndicationFeed): ...
