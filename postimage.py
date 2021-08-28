"""
Post an image to Mastodon
"""
from mastodon import Mastodon
import toml


def post_image(filename, alt, toot):
    config = toml.load('config.toml')['mastodon']

    mastodon = Mastodon(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        access_token=config['access_token'],
        api_base_url=config['url']
        )

    media_id = mastodon.media_post(filename, description=alt)
    mastodon.status_post(toot, media_ids=media_id, visibility='public')
