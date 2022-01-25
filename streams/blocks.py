"""Streamfields live in here."""
from django.db import models
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.fields import RichTextField, StreamField

class imageBlog(ImageChooserBlock):

    image = ImageChooserBlock(required=True)

    class Meta:  # noqa
        template = "streams/image_blog.html"
        icon = "image"
        label = "Image"

class RichtextBlog(blocks.RichTextBlock):
    """Richtext without (limited) all the features."""

    def __init__(
        self, required=True, help_text=None, editor="default", features=None, **kwargs
    ):  # noqa
        super().__init__(**kwargs)
        self.features = ["bold", "italic", "link"]

    class Meta:  # noqa
        template = "streams/richtext_blog.html"
        icon = "edit"
        label = "Simple RichText"