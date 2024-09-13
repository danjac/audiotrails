import http
import urllib.parse

import httpx
import pytest
from django.conf import settings
from django.core.signing import Signer
from django.urls import reverse, reverse_lazy

from radiofeed.http_client import Client
from radiofeed.tests.asserts import assert_200, assert_404


class TestIndex:
    url = reverse_lazy("index")

    @pytest.mark.django_db
    def test_anonymous(self, client):
        assert_200(client.get(self.url))

    @pytest.mark.django_db
    def test_authenticated(self, client, auth_user):
        response = client.get(self.url)
        assert response.url == settings.LOGIN_REDIRECT_URL


class TestManifest:
    @pytest.mark.django_db
    def test_get(self, client):
        assert_200(client.get(reverse("manifest")))


class TestAssetlinks:
    @pytest.mark.django_db
    def test_get(self, client):
        assert_200(client.get(reverse("assetlinks")))


class TestServiceWorker:
    @pytest.mark.django_db
    def test_get(self, client):
        assert_200(client.get(reverse("service_worker")))


class TestFavicon:
    @pytest.mark.django_db
    def test_get(self, client):
        assert_200(client.get(reverse("favicon")))


class TestRobots:
    @pytest.mark.django_db
    def test_get(self, client):
        assert_200(client.get(reverse("robots")))


class TestSecurty:
    @pytest.mark.django_db
    def test_get(self, client):
        assert_200(client.get(reverse("security")))


class TestAbout:
    @pytest.mark.django_db
    def test_get(self, client):
        assert_200(client.get(reverse("about")))


class TestPrivacy:
    @pytest.mark.django_db
    def test_get(self, client):
        assert_200(client.get(reverse("privacy")))


class TestAcceptGdprCookies:
    @pytest.mark.django_db
    def test_post(self, client):
        response = client.post(reverse("accept_gdpr_cookies"))
        assert_200(response)
        assert "accept-cookies" in response.cookies


class TestCoverImage:
    cover_url = "http://example.com/test.png"

    def get_url(self, size, url):
        return (
            reverse("cover_image", kwargs={"size": size})
            + "?"
            + urllib.parse.urlencode({"url": url})
        )

    def encode_url(self, url):
        return Signer().sign(url)

    @pytest.mark.django_db
    def test_ok(self, client, db, mocker):
        def _handler(request):
            return httpx.Response(http.HTTPStatus.OK, content=b"")

        mock_client = Client(transport=httpx.MockTransport(_handler))
        mocker.patch("radiofeed.views.get_client", return_value=mock_client)
        mocker.patch("PIL.Image.open", return_value=mocker.Mock())
        assert_200(client.get(self.get_url(96, self.encode_url(self.cover_url))))

    @pytest.mark.django_db
    def test_not_accepted_size(self, client, db, mocker):
        assert_404(client.get(self.get_url(500, self.encode_url(self.cover_url))))

    @pytest.mark.django_db
    def test_missing_url_param(self, client, db, mocker):
        assert_404(client.get(reverse("cover_image", kwargs={"size": 100})))

    @pytest.mark.django_db
    def test_unsigned_url(self, client, db):
        assert_404(client.get(self.get_url(96, self.cover_url)))

    @pytest.mark.django_db
    def test_failed_download(self, client, db, mocker):
        def _handler(request):
            raise httpx.HTTPError("invalid")

        mock_client = Client(transport=httpx.MockTransport(_handler))
        mocker.patch("radiofeed.views.get_client", return_value=mock_client)

        assert_200(client.get(self.get_url(96, self.encode_url(self.cover_url))))

    @pytest.mark.django_db
    def test_failed_process(self, client, db, mocker):
        def _handler(request):
            return httpx.Response(http.HTTPStatus.OK, content=b"")

        mock_client = Client(transport=httpx.MockTransport(_handler))
        mocker.patch("radiofeed.views.get_client", return_value=mock_client)
        mocker.patch("PIL.Image.open", side_effect=IOError())
        assert_200(client.get(self.get_url(96, self.encode_url(self.cover_url))))
