'use strict';

angular.module('papt.userservice', ['ngRoute'])

.factory('userService', ['$location', function($location) {
  var user;
  return {
    setUser: function(setTo) { user = setTo; },
    getUser: function() { return user; },
    checkLoggedIn: function() {
      console.log('checking logged in')
      if (user) {
        console.log("Logged in as " + user);
        return true;
      } else {
        console.log("Not logged in");
        $location.path('/login');
        return false;
      }
    }
  };
}]);
