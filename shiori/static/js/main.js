$(function() {
    var url_root = '/shiori/';
    function urlX(url) {if (/^https?:\/\//.test(url)) { return url; }}

    function idX(id) { return id; }

    function elem(tags, icon) {
        if (tags == undefined) {
            return '';
        } else {
            return '<p><i class="' + icon + '"></i> ' + tags + '</p>';
        }
    }

    function protect(state) {
        if (state) {
            return '<i class="icon-lock"></i> ';
        } else {
            return '';
        }
    }

    function get_page(url) {
        if (url) {
            var s = url.split('?')[1];
        } else {
            var s = location.search.substring(1);
        }
        var page;
        if (s) {
            var query = s.split('&');
            if (query != '') {
                query.forEach(function(val, index) {
                    if (query[index].match(/^page=/)) {
                        page = query[index].split('=')[1];
                    }
                });
            }
        }
        return page;
    }

    function search_link() {
        var search_query = '';
        if (search_word() != '') {
            search_query = '&q=' + search_word();
        }
        return search_query;
    }

    function render_pagination(meta) {
        var pager = '';
        if (meta.previous) {
            pager += ('<li><a href="?page=' +
                      get_page(meta.previous) +
                      '&is_all=' + is_all() +
                      search_link() +
                      '">&larr; previous</a></li>');
        }
        if (meta.next) {
            pager += ('<li><a href="?page=' +
                      get_page(meta.next) +
                      '&is_all=' + is_all() +
                      search_link() +
                      '">next &rarr;</a></li>');
        }
        return pager;
    }

    function display_message(el, msg, alert_type) {
        $('div#flash', el)
            .append('<div class="alert ' +
                    alert_type + '">' +
                    '<a class="close" data-dismiss="alert">x</a>' +
                    msg + '</div>');
    }

    function is_all() {
        var s = location.search.substring(1);
        var is_all;
        if (s) {
            var query = s.split('&');
            if (query != '') {
                query.forEach(function(val, index) {
                    if (query[index].match(/^is_all=/)) {
                        is_all = query[index].split('=')[1];
                    }
                });
            }
        }
        if (is_all == undefined) {
            is_all = 'false';
        }
        return is_all;
    }

    function search_word() {
        var s = location.search.substring(1);
        var search_word = '';
        if (query != '') {
            var query = s.split('&');
            query.forEach(function(val, index) {
                if (query[index].match(/^q=/)) {
                    search_word = query[index].split('=')[1];
                }
            });
        }
        return search_word;
    }

    var Category = Backbone.Model.extend({
        urlRoot: '/api/categories',
        idAttribute: 'id',
        defaults: {
            'category': ''
        },
        validate: function(attrs) {
            if (!attrs.category) {
                return 'required category.';
            }
        }
    });

    var CategoriesList = Backbone.Collection.extend({
        model: Category,
        url: '/api/categories',
        parse: function(res) {
            res.results.push({'meta': {'count': res.count,
                                       'next': res.next,
                                       'previous': res.previous}});
            return res.results;
        }
    });

    var CategoriesListView = Backbone.View.extend({
        el: $('div#categories_list'),
        initialize: function() {
            this.collection = new CategoriesList();
            this.listenTo(this.collection, 'add', this.appendItem);
            this.collection.fetch({data: {'page': get_page(),
                                          'is_all': is_all()}});
        },
        appendItem: function(item) {
            if (item.get('meta')) {
                this.pagination(item.get('meta'));
            } else {
                $(this.el)
                    .append('<a class="btn btn-primary" href="categories/' +
                            item.get('id') + '">' +
                            html_sanitize(item.get('category'), urlX, idX) +
                            '</a> ');
            }
        },
        pagination: function(meta) {
            $('ul.pager').append(render_pagination(meta));
        }
    });

    var CategoryView = Backbone.View.extend({
        el: $('div#category_view'),
        initialize: function() {
            var id = location.pathname.split('/')[3];
            this.model = new Category({id: id});
            this.bookmarks = new BookmarkList();
            this.listenTo(this.bookmarks, 'add', this.appendItem);
            this.listenTo(this.model, 'change', this.render);
            this.model.fetch();
        },
        events: {
            'mouseover a.btn': 'loadBookmark'
        },
        render: function() {
            var category = this.model.get('category');
            $('h4', this.el).append(category);
            this.bookmarks.fetch({data: {'page': get_page(),
                                         'is_all': is_all(),
                                         'categor': category}});
            return this;
        },
        appendItem: function(item) {
            if (item.get('meta')) {
                this.pagination(item.get('meta'));
            } else {
                $(this.el)
                    .append('<a rel="popover" class="btn btn-success" id="' +
                            html_sanitize(item.get('id'), urlX, idX) + '">' +
                            html_sanitize(item.get('title'), urlX, idX) +
                            '</a> ');
            }
        },
        loadBookmark: function(item) {
            var that = this;
            this.bookmark = new Bookmark({id: item.target.id});
            this.bookmark.fetch({
                data: {'is_all': is_all()},
                success: function() {
                    that.popup(that.bookmark);
                }
            });
        },
        popup: function(item) {
            $('a#' + item.id, this.el)
                .popover({title: protect(html_sanitize(item.get('is_hide'),
                                                       urlX, idX)) +
                          html_sanitize(item.get('title'), urlX, idX),
                          content: elem('<a href="' + item.get('url') +
                                        '">' +
                                        item.get('url') + '</a>',
                                        'icon-share') +
                          elem(item.get('description'), 'icon-comment') +
                          elem(item.get('tags'), 'icon-tags'),
                          trigger: 'manual',
                          delay: {show: 100, hide: 100}
                         }).click(function(e) {
                             $(this).popover('toggle');
                         });
        },
        pagination: function(meta) {
            $('ul.pager').append(render_pagination(meta));
        }
    });

    var BookmarkTags = Backbone.Model.extend({
        urlRoot: '/api/bookmark_tags',
        idAttribute: 'id',
        defaults: {
            'bookmark': '',
            'tag': ''
        }
    });

    var BookmarkTagsList = Backbone.Collection.extend({
        model: BookmarkTags,
        url: '/api/bookmark_tags',
        parse: function(res) {
            res.results.push({'meta': {'count': res.count,
                                       'next': res.next,
                                       'previous': res.previous}});
            return res.results;
        }
    });

    var Tag = Backbone.Model.extend({
        urlRoot: '/api/tags',
        idAttribute: 'id',
        defaults: {
            'tag': ''
        }
    });

    var TagsList = Backbone.Collection.extend({
        model: Tag,
        url: '/api/tags',
        parse: function(res) {
            res.results.push({'meta': {'count': res.count,
                                       'next': res.next,
                                       'previous': res.previous}});
            return res.results;
        }
    });

    var TagsListView = Backbone.View.extend({
        el: $('div#tags_list'),
        initialize: function() {
            this.collection = new TagsList();
            this.bookmark_tags = new BookmarkTagsList();
        },
        render: function() {
            var that = this;
            var used_tags = new Array();
            this.bookmark_tags.fetch({
                success: function() {
                    used_tags = _.uniq(that.bookmark_tags.pluck('tag'));
                }
            }).pipe(function() {
                var the = that;
                that.collection.fetch({
                    data: {'page': get_page(),
                           'is_all': is_all()},
                    success: function(item) {
                        that.collection.each(function(item) {
                            if (used_tags.indexOf(item.get('tag')) > -1) {
                                that.appendItem(item);
                            }
                        });
                    }
                });
            }, this);
            return this;
        },
        appendItem: function(item) {
            if (item.get('meta')) {
                this.pagination(item.get('meta'));
            } else {
                $(this.el)
                    .append('<a class="btn btn-info" href="tags/' +
                            item.get('id') + '">' +
                            html_sanitize(item.get('tag'), urlX, idX) +
                            '</a> ');
            }
        },
        pagination: function(meta) {
            $('ul.pager').append(render_pagination(meta));
        }
    });

    var TagView = Backbone.View.extend({
        el: $('div#tag_view'),
        initialize: function() {
            var id = location.pathname.split('/')[3];
            this.model = new Tag({id: id});
            this.bookmarks = new BookmarkList();
            this.listenTo(this.bookmarks, 'add', this.appendItem);
            this.listenTo(this.model, 'change', this.render);
            this.model.fetch();
        },
        events: {
            'mouseover a.btn': 'loadBookmark'
        },
        render: function() {
            var that = this;
            $(this.el).append('<h4>');
            $(this.el).append('<div>');
            var tag = this.model.get('tag');
            var tag_id = this.model.get('id');
            $('h4', this.el).append(tag);
            this.bookmarks.fetch({data: {'page': get_page(),
                                         'is_all': is_all(),
                                         'tag': tag}});
            return this;
        },
        appendItem: function(item) {
            if (item.get('meta')) {
                this.pagination(item.get('meta'));
            } else {
                $('div', this.el)
                    .append('<a rel="popover" class="btn btn-success" id="' +
                            html_sanitize(item.get('id'), urlX, idX) + '">' +
                            html_sanitize(item.get('title'), urlX, idX) +
                            '</a> ');
            }
        },
        pagination: function(meta) {
            $('ul.pager').append(render_pagination(meta));
        },
        loadBookmark: function(item) {
            var that = this;
            this.bookmark = new Bookmark({id: item.target.id});
            this.bookmark.fetch({
                data: {'is_all': is_all()},
                success: function() {
                    that.popup(that.bookmark);
                }
            });
        },
        popup: function(item) {
            $('a#' + item.id, this.el)
                .popover({title: protect(item.get('is_hide')) +
                          html_sanitize(item.get('title'), urlX, idX),
                          content: elem('<a href="' + item.get('url') +
                                        '">' +
                                        item.get('url') + '</a>',
                                        'icon-share') +
                          elem(html_sanitize(item.get('description'),
                                             urlX, idX),
                               'icon-comment') +
                          elem(html_sanitize(item.get('category'), urlX, idX),
                               'icon-book'),
                          trigger: 'manual',
                          delay: {show: 100, hide: 100}
                         }).click(function(e) {
                             $(this).popover('toggle');
                         });
        }
    });

    var Bookmark = Backbone.Model.extend({
        urlRoot: '/api/bookmarks',
        idAttribute: 'id',
        defaults: {
            url: '',
            title: '',
            category: '',
            description: '',
            is_hide: ''
        },
        validate: function(attrs) {
            if (!attrs.url) return 'required url.';
            if (!attrs.category) return 'required category.';
        }
    });

    var BookmarkList = Backbone.Collection.extend({
        model: Bookmark,
        url: '/api/bookmarks',
        parse: function(res) {
            res.results.push({'meta': {'count': res.count,
                                       'next': res.next,
                                       'previous': res.previous}});
            return res.results;
        }
    });

    var BookmarkListView = Backbone.View.extend({
        el: $('div#bookmark_list'),
        initialize: function() {
            this.collection = new BookmarkList();
            this.listenTo(this.collection, 'add', this.appendItem);
            this.collection.fetch({data: {'page': get_page(),
                                          'is_all': is_all(),
                                          'search': search_word()}});
        },
        events: {
            'mouseover a.btn': 'loadBookmark'
        },
        appendItem: function(item) {
            if (item.get('meta')) {
                this.pagination(item.get('meta'));
            } else {
                $(this.el)
                    .append('<a rel="popover" class="btn btn-success" id="' +
                            html_sanitize(item.get('id'), urlX, idX) + '">' +
                            html_sanitize(item.get('title'), urlX, idX) +
                            '</a> ');
            }
        },
        pagination: function(meta) {
            $('ul.pager').append(render_pagination(meta));
        },
        loadBookmark: function(item) {
            var that = this;
            this.bookmark = new Bookmark({id: item.target.id});
            this.bookmark.fetch({
                data: {'is_all': is_all()},
                success: function() {
                    that.popup(that.bookmark);
                }
            });
        },
        popup: function(item) {
            $('a#' + item.id, this.el)
                .popover({title: protect(item.get('is_hide')) +
                          html_sanitize(item.get('title'), urlX, idX),
                          content: elem('<a href="' + item.get('url') +
                                        '">' +
                                        item.get('url') + '</a>',
                                        'icon-share') +
                          elem(html_sanitize(item.get('description'),
                                             urlX, idX),
                               'icon-comment') +
                          elem('<a href="categories/' +
                               html_sanitize(item.get('category_id'),
                                             urlX, idX) +
                               '">' + html_sanitize(item.get('category'),
                                                    urlX, idX) + '</a>',
                               'icon-book') +
                          elem(html_sanitize(item.get('tags'), urlX, idX),
                               'icon-tags'),
                          trigger: 'manual',
                          delay: {show: 100, hide: 100}
                         }).click(function(e) {
                             $(this).popover('toggle');
                         });
        }
    });

    var AddBookmarkView = Backbone.View.extend({
        el: $('div#edit_view'),
        initialize: function() {
            this.categories = new CategoriesList();
            this.tags = new TagsList();
            this.bookmarks = new BookmarkList();
            this.bookmarkTags = new BookmarkTagsList();
        },
        events: {
            'keydown input#tags': 'save_tag',
            'click button:submit': 'add'
        },
        add: function(item) {
            var that = this;
            var registered_category;
            var category = html_sanitize(this.$('input#category').val(),
                                         urlX, idX);
            if (category.length == 0) {
                display_message(this.el, 'required category.', 'alert-success');
                return false;
            }

            this.categories.fetch({
                success: function() {
                    registered_category =
                        that.categories.where({'category': category});
                }
            }).pipe(function() {
                if (registered_category.length == 1) {
                    that.save_bookmark(category);
                } else {
                    that.category = new Category({
                        category: category
                    }, {collection: that.categories});
                    that.category.save(null, {
                        success: function() {
                            that.categories.add(that.category);
                        },
                        error: function(model, xhr, options) {
                            var obj = JSON.parse(xhr.responseText).category[0];
                            var msg = 'Category with this Category ' +
                                    'already exists.';
                            if (obj == msg) {
                                console.log(xhr.responseText);
                            }
                        }
                    }).pipe(function() {
                        that.save_bookmark(category);
                    }, this);
                }
            }, this);
            return this;
        },
        save_tag: function(event) {
            var that = this;
            if (event.keyCode == 13) {
                var tags_array = html_sanitize($('input#tags').val(),
                                               urlX, idX).split(',');

                if (tags_array.length > 0) {
                    $('input#tags', this.el)
                        .before('<span class="btn btn-mini tag ' +
                                tags_array[0] +
                                '">' + tags_array[0] + '</span>');
                    $('input#tags').val('');

                    this.tags.fetch({
                        success: function() {
                            registered_tag =
                                that.tags.where({'tag': tags_array[0]});
                        }
                    }).pipe(function() {
                        if (registered_tag.length == 1) {
                            $('span.' + tags_array[0], this.el)
                                .attr('id', registered_tag[0].id);
                        } else {
                            that.tag = new Tag({
                                tag: tags_array[0]
                            }, {collection: that.tags});
                            that.tag.save(null, {
                                success: function(_coll, _mdl, options) {
                                    that.tags.add(that.tag);
                                    console.log(options.xhr.responseText);
                                    $('span.' + tags_array[0], this.el)
                                        .attr('id', _mdl.id);
                                },
                                error: function(_mdl, xhr, options) {
                                    console.log(xhr.responseText);
                                    var obj = JSON.parse(
                                        xhr.responseText).tag[0];
                                }
                            });
                        }
                    });
                }
            }
        },
        save_bookmark: function(category) {
            var that = this;
            var url = this.$('input#url').val();
            var title = html_sanitize(this.$('input#title').val(), urlX, idX);

            var description = html_sanitize(
                this.$('textarea#description').val(), urlX, idX);
            if (this.$('input#is_hide').prop('checked')) {
                var is_hide = true;
            } else {
                var is_hide = false;
            }

            this.bookmarks.create({
                url: url,
                title: title,
                category: category,
                description: description,
                is_hide: is_hide
            }, {
                validate: true,
                success: function(_coll, _mdl, options) {
                    console.log(options.xhr.responseText);
                    this.$('span.tag').each(function(index, value) {
                        that.tagging_bookmark(_mdl.url, value.textContent);
                    });

                    display_message(this.el,
                                    options.xhr.statusText,
                                    'alert-success');
                },
                error: function(_coll, xhr, options) {
                    console.log(xhr.responseText);
                    display_message(this.el, xhr.responseText, 'alert-error');
                }
            });
        },
        tagging_bookmark: function(bookmark_url, tag) {
            this.bookmarkTags.create({
                bookmark: bookmark_url,
                tag: tag
            }, {
                validate: true,
                success: function(_coll, _mdl, options) {
                    console.log(options.xhr.responseText);
                },
                error: function(_coll, xhr, options) {
                    console.log(xhr.responseText);
                }
            });
        }
    });

    var BookmarkView = Backbone.View.extend({
        el: $('div#bookmark_view'),
        initialize: function() {
            var id = location.pathname.split('/')[3];
            this.model = new Bookmark({id: id});
            this.render();
        },
        render: function() {
            var that = this;
            this.model.fetch({
                data: {'is_all': is_all()},
                success: function(item) {
                    $('h2', this.el)
                        .text(html_sanitize(item.get('title'), urlX, idX));
                    $('h4 a#url', this.el)
                        .text(html_sanitize(item.get('url'), urlX, idX));
                    $('h4 a', this.el)
                        .attr('href',
                              html_sanitize(item.get('url'), urlX, idX));
                    $('p#desc', this.el)
                        .text(html_sanitize(item.get('description'),
                                            urlX, idX));
                    $('div#category > a.btn', this.el)
                        .text(html_sanitize(item.get('category'), urlX, idX));
                    $('div#category > a.btn', this.el)
                        .attr('href', url_root + 'categories/' +
                              html_sanitize(item.get('category_id'),
                                            urlX, idX));
                    if (item.get('tags').length > 0) {
                        item.get('tags').forEach(function(val, index) {
                            $('div#tags', this.el)
                                .append('<a class="btn btn-info"></a>');
                            $('div#tags > a.btn', this.el)
                                .text(html_sanitize(item.get('tags')[index]));
                        });
                    }

                }
            });
            return this;
        }
    });

    var FeedSubscription = Backbone.Model.extend({
        urlRoot: '/api/feed_subscription',
        idAttribute: 'id',
        defaults: {
            'url': '',
            'default_category': ''
        },
        validate: function(attrs) {
            if (!attrs.url) return 'required url.';
            if (!attrs.default_category) return 'required category.';
        }
    });

    var FeedSubscriptionList = Backbone.Collection.extend({
        model: FeedSubscription,
        url: '/api/feed_subscription',
        parse: function(res) {
            res.results.push({'meta': {'count': res.count,
                                       'next': res.next,
                                       'previous': res.previous}});
            return res.results;
        }
    });

    var FeedSubscriptionView = Backbone.View.extend({
        el: $('div#feed_subscription'),
        initialize: function() {
            this.collection = new FeedSubscriptionList();
            this.feed_subscriptions = new FeedSubscriptionList();
            this.listenTo(this.collection, 'add', this.appendItem);
            this.listenTo(this.collection, 'remove', this.removeItem);
            this.collection.fetch({data: {'page': get_page()}});
            this.categories = new CategoriesList();
        },
        events: {
            'click button#new_feed': 'show_modal',
            'click a#save': 'save',
            'click a#cancel': 'close_modal',
            'click a.btn-warning': 'edit',
            'click a.btn-danger': 'delete'
        },
        appendItem: function(item) {
            if (item.get('meta')) {
                this.pagination(item.get('meta'));
            } else {
                // This hack is prevent rendering without id, name;
                if (item.get('id') != undefined) {
                    $('tbody', this.el)
                        .append('<tr id="' + item.get('id') +
                                '"><td><a href="' +
                                html_sanitize(item.get('url'), urlX, idX) +
                                '">' +
                                html_sanitize(item.get('name'), urlX, idX) +
                                '</a></td><td>' +
                                html_sanitize(item.get('default_category'),
                                              urlX, idX) +
                                '</td><td>' +
                                /*
                                  // Todo: should implement this
                                <a class="btn btn-warning" id="edit_' +
                                item.get('id') +
                                '">edit</a> ' +
                                */
                                '<a class="btn btn-danger" id="delete_' +
                                item.get('id') +
                                '">delete</a></td></tr>');
                }
            }
        },
        pagination: function(meta) {
            $('ul.pager').append(render_pagination(meta));
        },
        show_modal: function() {
            $('div.modal', this.el).modal('show');
        },
        save: function() {
            var that = this;
            var registered_category;
            var category = html_sanitize(this.$('input#category').val(),
                                         urlX, idX);
            if (category.length == 0) {
                display_message(this.el, 'required category.', 'alert-error');
                return false;
            }
            this.categories.fetch({
                success: function() {
                    registered_category =
                        that.categories.where({'category': category});
                }
            }).pipe(function() {
                if (registered_category.length == 1) {
                    that.save_feed(category);
                } else {
                    that.category = new Category({
                        category: category
                    }, {collection: that.categories});
                    that.category.save(null, {
                        success: function() {
                            that.categories.add(that.category);
                        },
                        error: function(model, xhr, options) {
                            var obj = JSON.parse(xhr.responseText).category[0];
                            var msg = 'Category with this Category ' +
                                    'already exists.';
                            if (obj == msg) {
                                console.log(xhr.responseText);
                            }
                        }
                    }).pipe(function() {
                        that.save_feed(category);
                    }, this);
                }
            }, this);
            return this;
        },
        save_feed: function(category) {

            var that = this;
            var url = this.$('input#url').val();
            if (this.$('input#is_enabled').prop('checked')) {
                var is_enabled = true;
            } else {
                var is_enabled = false;
            }

            this.collection.create({
                url: url,
                default_category: category,
                is_enabled: is_enabled
            }, {
                validate: true,
                success: function(_coll, _mdl, options) {
                    console.log(options.xhr.responseText);
                    display_message(this.el,
                                    options.xhr.statusText,
                                    'alert-success');
                    // This hack is prevent rendering without id, name;
                    that.collection.add(that.collection.pop());
                },
                error: function(_coll, xhr, options) {
                    console.log(xhr.responseText);
                    display_message(this.el, xhr.responseText, 'alert-error');
                }
            });
            this.close_modal();
        },
        close_modal: function() {
            $('div.modal', this.el).modal('hide');
            $('input#url').val('');
            $('input#category').val('');
            $('input#is_enabled').attr('checked', true);
        },
        edit: function(event) {
            console.log(event.target.id);
        },
        delete: function(event) {
            var that = this;
            var id = event.target.id.split('delete_')[1];
            this.model = new FeedSubscription({id: id});
            this.collection.remove(this.model);
        },
        removeItem: function() {
            var that = this;
            this.model.destroy({
                success: function() {
                    display_message(this.el,
                                    'deleted: ' + that.model.get('id'),
                                   'alert-success');
                    $('tr#' + that.model.id, this.el).remove();
                }
            });
        }
    });

    var ProfileView = Backbone.View.extend({
        el: $('div#profile'),
        render: function() {
        }
    });

    var AppView = Backbone.View.extend({
        el: 'div#main',
        events: {
            'click a#login': 'login',
            'click a#logout': 'logout',
            'click a#add': 'add',
            'click a#profile': 'profile',
            'click a#categories': 'categories',
            'click a#tags': 'tags',
            'click span#search-btn': 'search',
            'click input#is_all': 'toggle_view'
        },
        initialize: function() {
        },
        login: function() {
            window.router.navigate('', true);
            return false;
        },
        logout: function() {
            window.router.navigate('index', true);
            return false;
        },
        add: function() {
            window.router.navigate('add', true);
            return false;
        },
        prifole: function() {
            window.router.navigate('profile', true);
            return false;
        },
        categories: function() {
            window.router.navigate('categories', true);
            return false;
        },
        category: function() {
            window.router.navigate('category', true);
            return false;
        },
        tags: function() {
            window.router.navigate('tags', true);
            return false;
        },
        tag: function() {
            window.router.navigate('tag', true);
            return false;
        },
        toggle_view: function(event) {
            if (is_all() == 'true') {
                location.href = location.pathname;
            } else {
                location.href = '?is_all=true';
            }
        },
        search: function(e) {
            if (location.pathname == '/shiori/search') {
                Backbone.history.fragment = null;
                Backbone.history.navigate(document.location.hash, true);
            }
            var path = 'search?q=' +
                $('input#search-word').val() +
                '&is_all=' + is_all();
            window.router.navigate(path, true);
            return false;
        },
        render: function() {
            $('div#submenu', this.el)
                .append('<a id="categories">Categories</a>')
                .append('<a id="tags">Tags</a>');
            if (is_all() == 'true') {
                $('input#is_all').attr('checked', true);
            } else {
                $('input#is_all').attr('checked', false);
            }
        }
    });

    var Router = Backbone.Router.extend({
        routes: {
            '': 'index',
            'openid/login': 'login',
            'logout': 'logout',
            'b/:id': 'bookmark',
            'add/': 'add',
            'profile': 'profile',
            'categories': 'categories',
            'categories/:id': 'category',
            'tags': 'tags',
            'tags/:id': 'tag',
            'feed_subscription': 'feed_subscription',
            'search': 'search'
        },

        index: function() {
            window.App.render();
            var bookmarkListView = new BookmarkListView();
            bookmarkListView.render();
        },
        login: function() {
        },
        profile: function() {
            window.App.render();
            var profileView = new ProfileView();
        },
        bookmark: function() {
            window.App.render();
            var bookmarkView = new BookmarkView();
        },
        add: function() {
            window.App.render();
            var addBookmarkView = new AddBookmarkView();
        },
        categories: function() {
            window.App.render();
            var categoriesListView = new CategoriesListView();
            categoriesListView.render();
        },
        category: function(id) {
            window.App.render();
            var categoryView = new CategoryView();
        },
        tags: function() {
            window.App.render();
            var tagsListView = new TagsListView();
            tagsListView.render();
        },
        tag: function() {
            window.App.render();
            var tagView = new TagView();
        },
        feed_subscription: function() {
            window.App.render();
            var feedSubscriptionView = new FeedSubscriptionView();
        },
        search: function() {
            window.App.render();
            var bookmarkListView = new BookmarkListView();
        }
    });

    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    $(document).ajaxSend(function(e, xhr, settings) {
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
    });

    window.router = new Router;
    window.App = new AppView;

    $(function() {
        Backbone.history.start({hashChange: false,
                                root: url_root});
    });
});
