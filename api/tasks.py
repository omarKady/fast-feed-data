from __future__ import absolute_import, unicode_literals
from celery import shared_task
from bs4 import BeautifulSoup
import requests
from .models import Feed
from django.core.mail import send_mail
from django.core.validators import URLValidator
validate = URLValidator()
import environ
env = environ.Env()
environ.Env.read_env()


# TODO : Check if feed item has rss/xml or not
def check_feed_has_rss(site_url):
    feed_links = []
    # For pages that rejects 'Get' requests that don't identify 'User-Agent'
    headers = {'User-Agent': ''}
    response = requests.get(site_url, headers=headers)
    # pass content (or document) to BeautifulSoup constructor to parse it
    soup = BeautifulSoup(response.text, "html.parser")
    # links is a list of "link" tags
    rss = soup.find_all("link", {"type":"application/rss+xml"})
    atom = soup.find_all("link", {"type":"application/atom+xml"})
    if rss:
        links = rss
    elif atom:
        links = atom
    else:
        return None

    for l in range(len(links)):
        # Check if 'href' has a URL not something like: " /feeds/ "
        try:
            validate(links[l].attrs['href'])
            feed_links.append(links[l].attrs['href'])
        except:
            print("String is not valid URL")
    return feed_links


# TODO : Send email to feed owner with update
def send_mail_to_owner(feed_item):
    owner = feed_item.owner
    title = feed_item.title
    feed_link = feed_item.feed_link
    if feed_link:
        msg = f'Congratolations your feed item : {title} was updated with feed link: {feed_link}'
    else:
        msg = f'Sorry your feed item {title} has no rss/xml feed'
    send_mail(
        f'Feed: {title} Update',
        msg,
        env('EMAIL_HOST_USER'),#From
        [owner],#To
        fail_silently=False,
    )


# TODO : Receive feed item id and update if it has rss/xml feed
@shared_task
def get_feed_to_check(id):
    url = Feed.objects.get(pk=id).url
    check_feed = check_feed_has_rss(url)
    #feed_item = Feed.objects.get(pk=id)
    if check_feed:
        feed = Feed.objects.get(pk=id)
        feed.feed_link = check_feed
        feed.save()
        feed_item = Feed.objects.get(pk=id)
        send_mail_to_owner(feed_item)
        return check_feed
    else:
        print(check_feed)
        feed_item = Feed.objects.get(pk=id)
        send_mail_to_owner(feed_item)
        return False
