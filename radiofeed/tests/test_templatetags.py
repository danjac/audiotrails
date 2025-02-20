import pytest
from django.contrib.sites.models import Site
from django.template.context import Context, RequestContext

from radiofeed.templatetags import absolute_uri, format_duration


@pytest.fixture
def req(rf, anonymous_user):
    req = rf.get("/")
    req.user = anonymous_user
    req.htmx = False
    req.site = Site.objects.get_current()
    return req


@pytest.fixture
def auth_req(req, user):
    req.user = user
    return req


class TestFormatDuration:
    @pytest.mark.parametrize(
        ("duration", "expected"),
        [
            pytest.param(0, "", id="zero"),
            pytest.param(30, "", id="30 seconds"),
            pytest.param(60, "1 minute", id="1 minute"),
            pytest.param(61, "1 minute", id="just over 1 minute"),
            pytest.param(90, "1 minute", id="1 minute 30 seconds"),
            pytest.param(540, "9 minutes", id="9 minutes"),
            pytest.param(2400, "40 minutes", id="40 minutes"),
            pytest.param(3600, "1 hour", id="1 hour"),
            pytest.param(
                9000,
                "2 hours 30 minutes",
                id="2 hours 30 minutes",
            ),
        ],
    )
    def test_format_duration(self, duration, expected):
        assert format_duration(duration) == expected


class TestAbsoluteUri:
    @pytest.mark.django_db
    def test_plain_url_from_request(self, rf):
        req = rf.get("/")
        assert (
            absolute_uri(RequestContext(req), "/podcasts/")
            == "http://example.com/podcasts/"
        )

    @pytest.mark.django_db
    def test_object_from_request(self, rf):
        req = rf.get("/")
        assert (
            absolute_uri(RequestContext(req), "/podcasts/")
            == "http://example.com/podcasts/"
        )

    @pytest.mark.django_db
    def test_plain_url_from_site(self, settings):
        settings.USE_HTTPS = False
        assert absolute_uri(Context(), "/podcasts/") == "http://example.com/podcasts/"

    @pytest.mark.django_db
    def test_https_from_site(self, settings):
        settings.USE_HTTPS = True
        assert absolute_uri(Context(), "/podcasts/") == "https://example.com/podcasts/"

    @pytest.mark.django_db
    def test_object_from_site(self, podcast, settings):
        settings.USE_HTTPS = False
        assert (
            absolute_uri(Context(), podcast)
            == f"http://example.com{podcast.get_absolute_url()}"
        )
