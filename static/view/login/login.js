'use strict';

angular.module('papt.login', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/login', {
    templateUrl: 'view/login/login.html',
    controller: 'LoginCtrl'
  });
}])

.controller('LoginCtrl', ['$rootScope', '$scope', '$location',
    function($rootScope, $scope, $location) {
  $scope.login = function() {
    if (!$scope.userid) {
      $scope.error = "Please enter a user ID.";
      return;
    }
    $scope.error = "";
    $rootScope.userid = $scope.userid;
    $location.path('/instructions');
  }
}]);
