(function(){
    var app = angular.module('home_feeds', ['ngResource']);

    app.controller('BlogFeedController', function($http, $log){
        var controller = this;

        controller.posts = [];

        var protocol = window.location.protocol;
        var host = window.location.host;
        var url = protocol + "//" + host + "/api/blog-feed/";

        $http.get(url).success(function(data, status, headers, config) {
            $log.info("Got blog feed");
            controller.posts = data;
        });

        controller.isNew = function(post) {
            var date = new Date(post.date);
            var now = new Date();

            // 604,800 seconds in a week * 1000 to get milliseconds
            return now - date < (604800 * 1000);
        }

        controller.empty = function() {
            return controller.posts.length == 0;
        };
    });

    app.controller('StatusFeedController', function($http, $log){
        var controller = this;

        controller.posts = [];

        var protocol = window.location.protocol;
        var host = window.location.host;
        var url = protocol + "//" + host + "/api/status-feed/";

        $http.get(url).success(function(data, status, headers, config) {
            $log.info("Got status feed");

            var categories = _.uniq(_.map(data, function(x){return x.category}));
            var posts = _.object(categories, _.map(categories, function(x){
                return _.filter(data, function(y) {
                    return y.category == x;
                })
            }));
            controller.posts = posts;
        });


        controller.empty = function() {
            return controller.posts.length == 0;
        };

        controller.classFor = function(post) {
            var cls = 'status-icon ';
            switch(post.tag){
            case 'OK':
                return cls + 'fa-check-circle green';
            case 'Down':
                return cls + 'fa-times-circle red';
            case 'Warning':
                return cls + 'fa-exclamation-triangle orange';
            default:
                return cls + 'fa-exclamation-circle';
            }
        }
    });


    app.filter('titlecase', function () {
        return function (input) {
            return _.chain(input.split(" "))
                .map(function(x) { return x.toLowerCase(); })
                .map(function(x) { return x.charAt(0).toUpperCase() + x.slice(1); })
                .reduce(function(x, y) { return x + " " + y; }, "")
                .value();
        }
    });

    app.filter('timeSince', function () {
        return function (input) {
            return moment(input).from(moment());
        }
    });
})();
