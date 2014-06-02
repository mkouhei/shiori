# -*- coding: utf-8 -*-
""" module django admin """
from django.contrib import admin
from shiori.bookmark.models import (Bookmark,
                                    Category,
                                    Tag,
                                    BookmarkTag,
                                    FeedSubscription,
                                    CrawlingHistory)


class BookmarkAdmin(admin.ModelAdmin):
    """ Customizing list display for Bookmark model """
    list_display = ('title', 'category', 'registered_datetime',
                    'owner', 'is_hide')


class BookmarkTagAdmin(admin.ModelAdmin):
    """ Customizing list display for BookmarkTag model """
    list_display = ('bookmark', 'tag')


class FeedSubscriptionAdmin(admin.ModelAdmin):
    """ Customizing list display for FeedSubscription model """
    list_display = ('name', 'owner', 'default_category')


class CrawlingHistoryAdmin(admin.ModelAdmin):
    """ Customizing list display for CrawlingHistory model """
    list_display = ('get_name', 'update_datetime', 'result')

    def get_name(self, obj):
        """ get feed name.
        Argument:
            obj: CrawlingHistory object
        Return:
            obj.feed.name
        """
        return obj.feed.name


admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(BookmarkTag, BookmarkTagAdmin)
admin.site.register(FeedSubscription, FeedSubscriptionAdmin)
admin.site.register(CrawlingHistory, CrawlingHistoryAdmin)
