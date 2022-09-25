"""
Post an image to Mastodon
"""
from mastodon import Mastodon
import toml
import argparse
import os


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Toot an image with its filename as the text')
    parser.add_argument('file', help='File')
    parser.add_argument('alt', help='Alt text')
    args = parser.parse_args()

    text = f'{os.path.splitext(os.path.basename(args.file))[0]}'
    post_image(args.file, args.alt, text)



