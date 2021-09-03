from django.urls import reverse

from jcasts.shared.assertions import assert_no_content, assert_ok


class TestRobots:
    def test_robots(self, db, client):
        assert_ok(client.get(reverse("robots")))


class TestHealthCheck:
    def test_health_check(self, db, client):
        assert_no_content(client.get(reverse("health_check")))


class TestAboutPages:
    def test_credits(self, db, client):
        assert_ok(client.get(reverse("about:credits")))

    def test_help(self, db, client):
        assert_ok(client.get(reverse("about:help")))

    def test_terms(self, db, client):
        assert_ok(client.get(reverse("about:terms")))


class TestErrorPages:
    def test_bad_request(self, db, client):
        assert_ok(client.get(reverse("error:bad_request")))

    def test_not_found(self, db, client):
        assert_ok(client.get(reverse("error:not_found")))

    def test_forbidden(self, db, client):
        assert_ok(client.get(reverse("error:forbidden")))

    def test_not_allowed(self, db, client):
        assert_ok(client.get(reverse("error:not_allowed")))

    def test_server_error(self, db, client):
        assert_ok(client.get(reverse("error:server_error")))

    def test_csrf(self, db, client):
        assert_ok(client.get(reverse("error:csrf")))


class TestAcceptCookies:
    def test_post(self, client, db):
        resp = client.post(reverse("accept_cookies"))
        assert_ok(resp)
        assert "accept-cookies" in resp.cookies
