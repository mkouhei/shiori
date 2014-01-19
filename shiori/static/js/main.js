$(function() {

	var Bookmark = Backbone.Model.extend({
		urlRoot: '/v1/bookmarks',
		idAttribute: 'id',
		defaults: {
			url: '',
			title: '',
			category: '',
			tags: '',
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
				.append('<thead><tr><th>title</th><th>uri</th><th>category</th></tr></thead>');
			$('table', this.el)
				.append('<tbody>');
			this.collection.each(function(item) {
				this.appendItem(item);
			}, this);
			return this;
		},
		appendItem: function(item) {
			$('table', this.el)
				.append('<tr id="' + item.id + '"><td><a href="' + item.get('url') + '">' + item.get('title') + '</a></td><td>' + item.get('url') + '</td><td>' + item.get('category') + '</td></tr>');
		}
	});

	var AppView = Backbone.View.extend({
		el: 'div#main',
		events: {
			'click a#login': 'login',
			'click a#logout': 'logout',
			'click a#profile': 'profile'
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
		}
	});

	var Router = Backbone.Router.extend({
		routes: {
			"": "index",
			"openid/login": "login",
			"logout": "logout",
			"profile": "profile"
		},
		index: function() {
			var bookmarkListView = new BookmarkListView();
			bookmarkListView.render();
		},
		login: function() {
		},
		profile: function() {
			var profileView = new ProfileView();
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
