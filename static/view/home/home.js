'use strict';

angular.module('papt.home', ['ngRoute', 'papt.userservice', 'papt.wordpairs'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/home', {
    templateUrl: 'view/home/home.html',
    controller: 'HomeCtrl'
  });
}])

.controller('HomeCtrl', ['$scope', '$location', 'userService', 'wordpairService', function($scope, $location, userService, wordpairService) {
  $scope.checkLoggedIn = userService.checkLoggedIn;
  $scope.showWordPairs = function(flavor) {
    wordpairService.setFlavor(flavor);
    $location.path('/wordpairs');
  };
}]);
