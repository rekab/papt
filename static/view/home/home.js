'use strict';

angular.module('papt.home', ['ngRoute', 'papt.userservice', 'papt.wordpairs'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/home', {
    templateUrl: 'view/home/home.html',
    controller: 'HomeCtrl'
  });
}])

.controller('HomeCtrl', ['$scope', 'userService', 'wordpairService', function($scope, userService, wordpairService) {
  $scope.checkLoggedIn = userService.checkLoggedIn;
  $scope.showWordPairs = function(flavor) {
    console.log('attempting to load flavor ' + flavor);
    wordpairService.goToWordpairPresentation(flavor);
  };
}]);
