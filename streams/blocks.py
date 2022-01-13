"""Streamfields live in here."""
from django.db import models
from wagtail.core.templatetags.wagtailcore_tags import RichText
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

class textAndImageBlock(blocks.StructBlock):
    """Cards with image and text and button(s)."""
    article = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("text", blocks.RichTextBlock(required=True, max_length=1000)),
                (
                    "button_url",
                    blocks.URLBlock(
                        required=False,
                        help_text="If the button page above is selected, that will be used first.",  # noqa
                    ),
                ),
            ]
        )
    )

    class Meta:  # noqa
        template = "streams/image_text_blog.html"
        icon = "placeholder"
        label = "Content Article"

class imageBlog(ImageChooserBlock):

    image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    class Meta:  # noqa
        template = "streams/image_blog.html"
        icon = "doc-full"
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
        