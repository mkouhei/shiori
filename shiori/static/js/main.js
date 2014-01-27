$(function() {

	var Category = Backbone.Model.extend({
		urlRoot: '/v1/categories',
		idAttribute: 'id',
		defaults: {
			'category': '',
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
				.append('<div id="' + item.id + '"><a href="' +
						item.get('id') + '">' + item.get('category') +
						'</a></div>');
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
		render: function() {
			var that = this;
			var selected_bookmarks = new Array();
			$(this.el).append('<h4>');
			$(this.el).append('<div>');
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
					console.log(selected_bookmarks[i].attributes);
					that.appendItem(selected_bookmarks[i]);
				}
			}, this);
			return this;
		},
		appendItem: function(item) {
			$('div', this.el)
				.append('<a id="' + item.get('id') +
						'"><span class="label label-info">' +
						item.get('title') + '</span></a> ');
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
				.append('<a href="' +	item.get('id') + '">' +
						item.get('tag') + '</a> ')
		}
	});

	var TagView = Backbone.View.extend({
		el: $('div#tag_view'),
		initialize: function() {
			var id = location.pathname.split('/')[3];
			this.model = new Tag({id: id});
			this.render();
		},
		render: function() {
			var that = this;
			$(this.el).append('<h4>');
			$(this.el).append('<dl>');
			this.model.fetch({
				success: function() {
					$('h4', this.el).append(that.model.get('tag'));
				}
			});
			return this;
		}
	});

	var Bookmark = Backbone.Model.extend({
		urlRoot: '/v1/bookmarks',
		idAttribute: 'id',
		defaults: {
			url: '',
			title: '',
			category: '',
			registered_datetime: '',
			last_modified: '',
			description: '',
			owner: '',
			is_hide: ''
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
		render: function() {
			var that = this;
			$(this.el)
				.append('<table class="table table-striped table-bordered table-condensed">');
			$('table', this.el)
				.append('<thead><tr><th>title</th><th>uri</th><th>category</th><th>tags</th></tr></thead>');
			$('table', this.el)
				.append('<tbody>');
			this.collection.each(function(item) {
				this.appendItem(item);
			}, this);
			return this;
		},
		appendItem: function(item) {
			$('table', this.el)
				.append('<tr id="' + item.id + '"><td><a href="' +
						item.get('url') + '">' + item.get('title') +
						'</a></td><td>' + item.get('url') +
						'</td><td><a href="categories/' + item.get('category_id') + '">' +
						item.get('category') + '</a></td><td>' + item.get('tags') +
						'</td></tr>');
		}
	});

	var AppView = Backbone.View.extend({
		el: 'div#main',
		events: {			'click a#login': 'login',
			'click a#logout': 'logout',
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
			"profile": "profile",
			"categories/": "categories",
			"categories/:id": "category",
			"tags/": "tags",
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
			var profileView = new ProfileView();
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
