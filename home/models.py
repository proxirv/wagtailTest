from django.db import models

from wagtail.core.models import Page


class HomePage(Page):
    """pass"""
    template = "blog/blog_listing_page.html"
    max_cout = 1
