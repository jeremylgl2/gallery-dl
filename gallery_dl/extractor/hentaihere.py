# -*- coding: utf-8 -*-

# Copyright 2016-2017 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extract hentai-manga from https://hentaihere.com/"""

from .common import MangaExtractor
from .. import text
from . import hentaicdn
import re


class HentaihereMangaExtractor(MangaExtractor):
    """Extractor for hmanga from hentaihere.com"""
    category = "hentaihere"
    pattern = [r"(?:https?://)?(?:www\.)?(hentaihere\.com/m/S\d+)/?$"]
    scheme = "https"
    test = [
        ("https://hentaihere.com/m/S13812", {
            "url": "d1ba6e28bb2162e844f8559c2b2725ba0a093559",
        }),
        ("https://hentaihere.com/m/S7608", {
            "url": "6c5239758dc93f6b1b4175922836c10391b174f7",
        }),
    ]

    def chapters(self, page):
        return list(text.extract_iter(
            page, '<li class="sub-chp clearfix">\n<a href="', '"'
        ))


class HentaihereChapterExtractor(hentaicdn.HentaicdnChapterExtractor):
    """Extractor for a single manga chapter from hentaihere.com"""
    category = "hentaihere"
    pattern = [r"(?:https?://)?(?:www\.)?hentaihere\.com/m/S(\d+)/(\d+)"]
    test = [("https://hentaihere.com/m/S13812/1/1/", {
        "url": "964b942cf492b3a129d2fe2608abfc475bc99e71",
        "keyword": "7b31d19668b353f7be73b330a52ec6a7e56d23ea",
    })]

    def __init__(self, match):
        hentaicdn.HentaicdnChapterExtractor.__init__(self)
        self.gid, self.chapter = match.groups()
        self.url = "https://hentaihere.com/m/S{}/{}/1".format(
            self.gid, self.chapter
        )

    def get_job_metadata(self, page, images):
        title = text.extract(page, "<title>", "</title>")[0]
        pattern = r"Page 1 \| (.+) \(([^)]+)\) - Chapter \d+: (.+) by (.+) at "
        match = re.match(pattern, title)
        return {
            "manga_id": self.gid,
            "manga": match.group(1),
            "type": match.group(2),
            "chapter": self.chapter,
            "title": match.group(3),
            "author": match.group(4),
            "count": len(images),
            "lang": "en",
            "language": "English",
        }
