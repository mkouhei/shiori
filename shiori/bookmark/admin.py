# -*- coding: utf-8 -*-
from django.contrib import admin
from shiori.bookmark.models import (Bookmark,
                                    Category,
                                    Tag,
                                    BookmarkTag,
                                    FeedSubscription,
                                    CrawlingHistory)


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'registered_datetime',
                    'owner', 'is_hide')


class BookmarkTagAdmin(admin.ModelAdmin):
    list_display = ('bookmark', 'tag')


class FeedSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'default_category')


class CrawlingHistoryAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'update_datetime', 'result')

    def get_name(self, obj):
        return obj.feed.name


admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(BookmarkTag, BookmarkTagAdmin)
admin.site.register(FeedSubscription, FeedSubscriptionAdmin)
admin.site.register(CrawlingHistory, CrawlingHistoryAdmin)
