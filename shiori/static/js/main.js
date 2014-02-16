$(function() {
    function urlX(url) {if(/^https?:\/\//.test(url)) {return url }}
    function idX(id) { return id }

	function elem(tags, icon) {
		if (tags.length > 0) {
			return '<p><i class="' + icon + '"></i> ' + tags + '</p>';
		} else {
			return '';
		}
	}

	function protect(state) {
		if (state) {
			return '<i class="icon-lock"></i> ';
		} else {
			return '';
		}
	}

	var Category = Backbone.Model.extend({
		urlRoot: '/v1/categories',
		idAttribute: 'id',
		defaults: {
			'category': '',
		},
		validate: function(attrs) {
			if (!attrs.category) return "required category.";
		}
	});

	var CategoriesList = Backbone.Collection.extend({
		model: Category,
		url: '/v1/categories',
		parse: function(res) {
			return res.results;
		}
	});

	var CategoriesListView = Backbone.View.extend({
		el: $('div#categories_list'),
		initialize: function() {
			this.collection = new CategoriesList();
			this.listenTo(this.collection, 'add', this.appendItem);
			this.collection.fetch();
		},
		render: function() {
			this.collection.each(function(item) {
				this.appendItem(item);
			}, this);
			return this;
		},
		appendItem: function(item) {
			$(this.el)
				.append('<a class="btn btn-primary" href="categories/' +
						item.get('id') + '">' +
						html_sanitize(item.get('category'), urlX, idX) +
						'</a> ');
		}
	});

	var CategoryView = Backbone.View.extend({
		el: $('div#category_view'),
		initialize: function() {
			var id = location.pathname.split('/')[3];
			this.model = new Category({id: id});
			this.bookmarks = new BookmarkList();
			this.render();
		},
		events: {
			'mouseover a.btn': 'loadBookmark'
		},
		render: function() {
			var that = this;
			var selected_bookmarks = new Array();
			this.model.fetch({
				success: function() {
					$('h4', this.el).append(that.model.get('category'));
				}
			}, this);
			this.bookmarks.fetch({
				success: function() {
					selected_bookmarks = that.bookmarks.where(
						{'category': that.model.get('category')});
					
				}
			}).pipe(function() {
				for (var i = 0; i < selected_bookmarks.length; i++) {
					that.appendItem(selected_bookmarks[i]);
				}
			}, this);
			return this;
		},
		appendItem: function(item) {
			$(this.el)
				.append('<a rel="popover" class="btn btn-success" id="' +
						html_sanitize(item.get('id'), urlX, idX) + '">' +
						html_sanitize(item.get('title'), urlX, idX) +
						'</a> ');
		},
		loadBookmark: function(item) {
			var that = this;
			this.bookmark = new Bookmark({id: item.target.id});
			this.bookmark.fetch({
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
						  delay: {hide: 3000}
						 });
		}
	});

	var BookmarkTags = Backbone.Model.extend({
		urlRoot: '/v1/bookmark_tags',
		idAttribute: 'id',
		defaults: {
			'bookmark': '',
			'tag': ''
		}
	});

	var BookmarkTagsList = Backbone.Collection.extend({
		model: BookmarkTags,
		url: '/v1/bookmark_tags',
		parse: function(res) {
			return res.results;
		}
	});

	var Tag = Backbone.Model.extend({
		urlRoot: '/v1/tags',
		idAttribute: 'id',
		defaults: {
			'tag': ''
		}
	});

	var TagsList = Backbone.Collection.extend({
		model: Tag,
		url: '/v1/tags',
		parse: function(res) {
			return res.results;
		}
	});

	var TagsListView = Backbone.View.extend({
		el: $('div#tags_list'),
		initialize: function() {
			this.collection = new TagsList();
			this.collection.fetch();
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
				that.collection.each(function(item) {
					if (used_tags.indexOf(item.get('tag')) > -1) {
						that.appendItem(item);
					}
				});
			}, this);
			return this;
		},
		appendItem: function(item) {
			$(this.el)
				.append('<a class="btn btn-info" href="tags/' +
						item.get('id') + '">' +
						html_sanitize(item.get('tag'), urlX, idX) + '</a> ');
		}
	});

	var TagView = Backbone.View.extend({
		el: $('div#tag_view'),
		initialize: function() {
			var id = location.pathname.split('/')[3];
			this.model = new Tag({id: id});
			this.bookmarks = new BookmarkList();
			this.render();
		},
		events: {
			'mouseover a.btn': 'loadBookmark'
		},
		render: function() {
			var that = this;
			var selected_bookmarks = new Array();
			$(this.el).append('<h4>');
			$(this.el).append('<div>');
			this.model.fetch({
				success: function() {
					$('h4', this.el).append(that.model.get('tag'));
				}
			}, this);
			this.bookmarks.fetch({
				success: function() {
					that.bookmarks.find(function(item) {
						if (item.get('tags').indexOf(that.model.get('tag')) > -1) {
							selected_bookmarks.push(item);
						}
					});
				}
			}).pipe(function() {
				for (var i = 0; i < selected_bookmarks.length; i++) {
					that.appendItem(selected_bookmarks[i]);
				}
			}, this);
			return this;
		},
		appendItem: function(item) {
			$('div', this.el)
				.append('<a rel="popover" class="btn btn-success" id="' +
						html_sanitize(item.get('id'), urlX, idX) + '">' +
						html_sanitize(item.get('title'), urlX, idX) +
						'</a> ');
		},
		loadBookmark: function(item) {
			var that = this;
			this.bookmark = new Bookmark({id: item.target.id});
			this.bookmark.fetch({
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
						  elem(html_sanitize(item.get('description'), urlX, idX),
							   'icon-comment') +
						  elem(html_sanitize(item.get('category'), urlX, idX),
							   'icon-book'),
						  delay: {hide: 3000}
						 });
		}
	});

	var Bookmark = Backbone.Model.extend({
		urlRoot: '/v1/bookmarks',
		idAttribute: 'id',
		defaults: {
			url: '',
			title: '',
			category: '',
			description: '',
			is_hide: ''
		},
		validate: function(attrs) {
			if (!attrs.url) return "required url.";
			if (!attrs.category) return "required category.";
		}
	});

	var BookmarkList = Backbone.Collection.extend({
		model: Bookmark,
		url: '/v1/bookmarks',
		parse: function(res) {
			return res.results;
		}
	});

	var BookmarkListView = Backbone.View.extend({
		el: $('div#bookmark_list'),
		initialize: function() {
			this.collection = new BookmarkList();
			this.listenTo(this.collection, 'add', this.appendItem);
			this.collection.fetch();
		},
		events: {
			'mouseover a.btn': 'loadBookmark'
		},
		render: function() {
			var that = this;
			this.collection.each(function(item) {
				this.appendItem(item);
			}, this);
			return this;
		},
		appendItem: function(item) {
			$(this.el)
				.append('<a rel="popover" class="btn btn-success" id="' +
						html_sanitize(item.get('id'), urlX, idX) + '">' +
						html_sanitize(item.get('title'), urlX, idX) +
						'</a> ');
		},
		loadBookmark: function(item) {
			var that = this;
			this.bookmark = new Bookmark({id: item.target.id});
			this.bookmark.fetch({
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
						  elem(html_sanitize(item.get('description'), urlX, idX),
							   'icon-comment') + 
						  elem('<a href="categories/' +
							   html_sanitize(item.get('category_id'), urlX, idX) +
							   '">' + html_sanitize(item.get('category'),
													urlX, idX) + '</a>',
							   'icon-book') +
						  elem(html_sanitize(item.get('tags'), urlX, idX),
							   'icon-tags'),
						  delay: {hide: 3000}
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
			var category = html_sanitize(this.$('input#category').val(), urlX, idX);
			if (category.length == 0) {
				$('div#flash', this.el)
				.append('<div class="alert alert-error">' +
						'<a class="close" data-dismiss="alert">x</a>' +
						'required category.</div>');
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
							if (obj == "Category with this Category already exists.") {
								console.log(xhr.responseText);
							}
						}
					}).pipe(function() {
						that.save_bookmark(category)
					}, this);
				}
			}, this);
			return this;
		},
		save_tag: function(event) {
			var that = this;
			if (event.keyCode == 13) {
				var tags_array = html_sanitize($('input#tags').val(), urlX, idX).split(',');

				if (tags_array.length > 0) {
					$('input#tags', this.el)
						.before('<span class="btn btn-mini tag ' + tags_array[0] +
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
									var obj = JSON.parse(xhr.responseText).tag[0];
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

			var description = html_sanitize(this.$('textarea#description').val(), urlX, idX);
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
					console.log(options.xhr.responseText)
					this.$('span.tag').each(function(index, value) {
						that.tagging_bookmark(_mdl.url, value.textContent);
					});

					$('div#flash', this.el)
						.append('<div class="alert alert-success">' +
								'<a class="close" data-dismiss="alert">x</a>' +
								options.xhr.statusText + '</div>');
				},
				error: function(_coll, xhr, options) {
					console.log(xhr.responseText);
					$('div#flash', this.el)
						.append('<div class="alert alert-error">' +
								'<a class="close" data-dismiss="alert">x</a>' +
								xhr.responseText + '</div>');

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
				success: function(item) {
					$('h2', this.el)
						.text(html_sanitize(item.get('title'), urlX, idX));
					$('h4 a#url', this.el)
						.text(html_sanitize(item.get('url'), urlX, idX));
					$('h4 a', this.el)
						.attr('href', html_sanitize(item.get('url'), urlX, idX));
					$('p#desc', this.el)
						.text(html_sanitize(item.get('description'), urlX, idX));
					$('div#category > a.btn', this.el)
						.text(html_sanitize(item.get('category'), urlX, idX));
					$('div#category > a.btn', this.el)
						.attr('href', '/shiori/categories/' +
							  html_sanitize(item.get('category_id'), urlX, idX));
					if (item.get('tags').length > 0) {
						for (var i = 0; i < item.get('tags').length; i++) {
							$('div#tags', this.el)
								.append('<a class="btn btn-info"></a>');
							$('div#tags > a.btn', this.el)
								.text(html_sanitize(item.get('tags')[i]));
						}
					}

				}
			});
			return this;
		}
	});

	var ProfileView = Backbone.Router.extend({
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
			'click a#tags': 'tags'
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
		render : function() {
			$('div#submenu', this.el)
				.append('<a id="categories">Categories</a>')
				.append('<a id="tags">Tags</a>');
		}
	});

	var Router = Backbone.Router.extend({
		routes: {
			"": "index",
			"openid/login": "login",
			"logout": "logout",
			"b/:id": "bookmark",
			"add/": "add",
			"profile": "profile",
			"categories": "categories",
			"categories/:id": "category",
			"tags": "tags",
			"tags/:id": "tag"
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
								root: "/shiori"})
	});
});
