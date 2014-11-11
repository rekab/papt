'use strict';

angular.module('papt.userservice', ['ngRoute'])

.factory('userService', ['$location', function($location) {
  var user, csrfToken;
  return {
    setUser: function(newUser, newToken) { 
      user = newUser; 
      csrfToken = newToken;
    },
    getUser: function() { return user; },
    getCsrfToken: function() { return csrfToken; },
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
