'use strict';

angular.module('papt.home', ['ngRoute', 'papt.wordpairs'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/home', {
    templateUrl: 'view/home/home.html',
    controller: 'HomeCtrl'
  });
}])

.controller('HomeCtrl', ['$scope', '$location', 'wordpairService', function($scope, $location, wordpairService) {
  $scope.checkLoggedIn = function() {
    console.log('checking logged in')
    if (!$scope.userid) {
      console.log("Not logged in");
      $location.path('/login');
      return;
    }
  };
  $scope.showWordPairs = function(flavor) {
    wordpairService.setFlavor(flavor);
    $location.path('/wordpairs');
  };
}]);
