from django.db import models
"""from wagtail.core import blocks"""
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page,Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    StreamFieldPanel,
)
from modelcluster.fields import ParentalKey
from streams import blocks 

class BlogCategoriesOrderable(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("blog.PostPage", related_name="blog_categories",null=True)
    categories = models.ForeignKey(
        "blog.BlogCategories",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("categories"),
    ]

class BlogCategories(models.Model):
    """Snippets."""

    categories = models.CharField(max_length=100)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("categories"),
            ],
            heading="Categorie(s)",
        )
    ]

    def __str__(self):
        """String repr of this class."""
        return self.categories

    class Meta:  # noqa
        verbose_name = "Categories of artile"
        verbose_name_plural = "Categories of articles"

register_snippet(BlogCategories)

class BlogPage(Page):
    titlearticles = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("titlearticles", classname="full"),
    ]

class PostPage(Page):
    custontitle = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    text = RichTextField(
        max_length=250,
        blank=True,
        null=True,
    )
    summary = StreamField(
        [
            ("text_blog",blocks.RichtextBlog()),
            ("image_blog",blocks.imageBlog()),
        ],
        null=True,
        blank=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("custontitle"),
        FieldPanel("text"),
        ImageChooserPanel("image"),
        StreamFieldPanel("summary"),
        MultiFieldPanel(
            [
                InlinePanel("blog_categories", label="categorie", min_num=1, max_num=3),
            ],
            heading="Categorie(s)",
        ),
    ]
