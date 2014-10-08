'use strict';

console.log('loading logincheck module');
angular.module('papt.logincheck', [])
.factory('loginCheck', ['$location', function($location) {
  console.log('what');
  return function(scope) {
    if (!scope.userid) {
      console.log("Not logged in");
      $location.path('/login');
      return;
    }
  };
}]);
