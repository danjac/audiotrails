import itertools

import lxml

from django import forms

from radiofeed.common.utils.xml import parse_xml, xpath_finder
from radiofeed.podcasts.models import Podcast, Subscription
from radiofeed.users.models import User


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("send_email_notifications",)
        help_texts = {
            "send_email_notifications": "I'd like to receive notications of new content and recommendations.",
        }


class OpmlUploadForm(forms.Form):
    opml = forms.FileField(
        label="Select OPML file",
        widget=forms.FileInput(
            attrs={
                "accept": ",".join(
                    [
                        ".opml",
                        ".xml",
                        "application/xml",
                        "text/x-opml",
                        "text/xml",
                    ]
                )
            }
        ),
    )

    def subscribe_to_feeds(self, user, limit=300):
        """Subscribes user to feeds in uploaded OPML.

        Args:
            user (User)
            limit (int): limit of OPML feeds

        Returns:
            int: number of new subscribed feeds
        """

        return len(
            Subscription.objects.bulk_create(
                [
                    Subscription(podcast=podcast, user=user)
                    for podcast in itertools.islice(
                        Podcast.objects.filter(rss__in=self.parse_opml())
                        .exclude(subscription__user=user)
                        .distinct(),
                        limit,
                    )
                ],
                ignore_conflicts=True,
            )
        )

    def parse_opml(self):
        self.cleaned_data["opml"].seek(0)

        try:
            for element in parse_xml(self.cleaned_data["opml"].read(), "outline"):
                with xpath_finder(element) as finder:
                    if rss := finder.first("@xmlUrl"):
                        yield rss
        except lxml.etree.XMLSyntaxError:
            return
