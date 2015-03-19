(function(){
    var app = angular.module('home_feeds', ['ngResource']);

    app.controller('BlogFeedController', function($http, $log){
        var controller = this;

        controller.posts = [];

        protocol = window.location.protocol;
        host = window.location.host;
        url = protocol + "//" + host + "/api/blog-feed/";

        $http.get(url).success(function(data, status, headers, config) {
            $log.info("Got blog feed");
            $log.debug(data);
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

        protocol = window.location.protocol;
        host = window.location.host;
        url = protocol + "//" + host + "/api/status-feed/";

        $http.get(url).success(function(data, status, headers, config) {
            $log.info("Got status feed");
            $log.debug(data);
            controller.posts = data;
        });

        controller.empty = function() {
            return controller.posts.length == 0;
        };

        controller.classFor = function(post) {
            cls = 'status-icon ';
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

})();
