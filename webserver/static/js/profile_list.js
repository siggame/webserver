(function(){
  var app = angular.module('profile_list', ['ngResource']);
  app.controller('ProfileListController', function($http){
    controller = this;

    controller.profiles = [];

    protocol = window.location.protocol;
    host = window.location.host;
    url = protocol + "//" + host + "/api/profiles/";

    $http.get(url).success(function(data, status, headers, config) {
      controller.profiles = data;
    });

    controller.empty = function() {
      return controller.profiles.length == 0;
    };
  });

})();
