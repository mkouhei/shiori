$(function() {
	window.router = new Router;
	window.App = new AppView;

	$(function() {
		Backbone.history.start({hashChange: false,
								root: "/shiori"})
	});
});
