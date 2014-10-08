'use strict';

angular.module('papt.testinstructions', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/testinstructions', {
    templateUrl: 'view/testinstructions/testinstructions.html',
    controller: 'TestInstructionsCtrl'
  });
}])

.controller('TestInstructionsCtrl', ['$scope', '$location', function($scope, $location) {
  $scope.checkLoggedIn = function() {
    console.log('checking logged in')
    if (!$scope.userid) {
      console.log("Not logged in");
      $location.path('/login');
      return;
    }
  };
  $scope.proceed = function() {
    $location.path('/test');
  };
}]);
