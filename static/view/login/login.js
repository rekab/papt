'use strict';

angular.module('papt.login', ['ngRoute', 'papt.userservice'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/login', {
    templateUrl: 'view/login/login.html',
    controller: 'LoginCtrl'
  });
}])

.controller('LoginCtrl', ['$scope', '$location', '$http', 'userService',
    function($scope, $location, $http, userService) {
  $scope.login = function() {
    if (!$scope.userid) {
      $scope.error = "Please enter a user ID.";
      return;
    }
    $http.post('/user/login', {username: $scope.userid}).then(function(response) {
      console.log('Successfully logged in')
      $scope.error = "";
      userService.setUser($scope.userid, response.data.csrf_token);
      $location.path('/home');
    }, function(failureResponse) {
      console.log('Login failure: ' + failureResponse);
      $scope.error = failureResponse.data.error || "Server errror";
    });
  }
}])

