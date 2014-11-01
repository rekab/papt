'use strict';

angular.module('papt.login', ['ngRoute', 'papt.userservice'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/login', {
    templateUrl: 'view/login/login.html',
    controller: 'LoginCtrl'
  });
}])

.controller('LoginCtrl', ['$scope', '$location', 'userService',
    function($scope, $location, userService) {
  $scope.login = function() {
    if (!$scope.userid) {
      $scope.error = "Please enter a user ID.";
      return;
    }
    $scope.error = "";
    userService.setUser($scope.userid);
    $location.path('/home');
  }
}])

