'use strict';

angular.module('papt.done', ['ngRoute', 'papt.userservice'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/done', {
    templateUrl: 'view/done/done.html',
    controller: 'DoneCtrl'
  });
}])

.controller('DoneCtrl', ['userService', '$scope', '$location',
    function(userService, $scope, $location) {
  $scope.checkLoggedIn = userService.checkLoggedIn;
  $scope.proceed = function() {
    $location.path('/home');
  };
}]);
