'use strict';

angular.module('papt.instructions', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/instructions', {
    templateUrl: 'view/instructions/instructions.html',
    controller: 'InstructionsCtrl'
  });
}])

.controller('InstructionsCtrl', ['$scope', '$location', function($scope, $location) {
  $scope.checkLoggedIn = function() {
    if (!$scope.userid) {
      console.log("Not logged in");
      $location.path('/login');
      return;
    }
  };
  $scope.proceed = function() {
    $location.path('/wordpairs');
  };
}]);
