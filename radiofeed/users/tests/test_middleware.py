from __future__ import annotations

from django.conf import settings

from radiofeed.users.factories import create_user
from radiofeed.users.middleware import language_middleware


class Testlanguage_middleware:
    def test_anonymous(self, rf, get_response, anonymous_user):
        req = rf.get("/")
        req.user = anonymous_user
        resp = language_middleware(get_response)(req)
        assert settings.LANGUAGE_COOKIE_NAME not in resp.cookies

    def test_authenticated(self, db, rf, get_response):

        req = rf.get("/")
        req.user = create_user(language="fi")
        resp = language_middleware(get_response)(req)
        assert resp.cookies[settings.LANGUAGE_COOKIE_NAME].value == "fi"
