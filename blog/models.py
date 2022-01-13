from django.db import models
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
from django.shortcuts import render
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from streams import blocks
from modelcluster.fields import ParentalKey

class BlogCategoriesOrderable(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("blog.BlogDetailPage", related_name="blog_categories_article",null=True)
    auxpage = ParentalKey("blog.BlogListingPage", related_name="blog_categories_listing",null=True)
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
            heading="Categories of Article",
        )
    ]

    def __str__(self):
        """String repr of this class."""
        return self.categories

    class Meta:  # noqa
        verbose_name = "Categories of artile"
        verbose_name_plural = "Categories of articles"

register_snippet(BlogCategories)

class BlogListingPage(Page):
    """Listing page lists all the Blog Detail Pages."""

    template = "blog/blog_listing_page.html"

    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel("blog_image"),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogDetailPage.objects.live().public()
        return context

class BlogDetailPage(Page):
    """Blog detail page."""
    
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    contentt = StreamField(
        [
            ("text_blog",blocks.RichtextBlog()),
            ("image_blog",blocks.imageBlog()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel("blog_image"),
        StreamFieldPanel("contentt"),
    ]