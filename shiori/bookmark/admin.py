# -*- coding: utf-8 -*-
from django.contrib import admin
from shiori.bookmark.models import (Bookmark,
                                    Category,
                                    Tag,
                                    BookmarkTag,
                                    FeedSubscription,
                                    CrawlingHistory)


admin.site.register(Bookmark)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(BookmarkTag)
admin.site.register(FeedSubscription)
admin.site.register(CrawlingHistory)
