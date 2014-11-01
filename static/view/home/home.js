'use strict';

angular.module('papt.home', ['ngRoute', 'papt.userservice', 'papt.wordpairs', 'papt.test'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/home', {
    templateUrl: 'view/home/home.html',
    controller: 'HomeCtrl'
  });
}])

.controller('HomeCtrl', ['$scope', 'userService', 'wordpairService', 'testService', function($scope, userService, wordpairService, testService) {
  $scope.checkLoggedIn = userService.checkLoggedIn;
  $scope.showWordPairs = function(flavor) {
    console.log('attempting to load wordpair flavor ' + flavor);
    wordpairService.goToWordpairPresentation(flavor);
  };
  $scope.startTest = function(flavor) {
    console.log('attempting to load test flavor ' + flavor);
    testService.goToTest(flavor);
  };
}]);
