'use strict';

angular.module('papt.test', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/test', {
    templateUrl: 'view/test/test.html',
    controller: 'TestCtrl'
  });
}])

.controller('TestCtrl', ['$scope', '$location', '$http', function($scope, $location, $http) {
  $scope.start = function() {
    if (!$scope.userid) {
      console.log("Not logged in");
      //$location.path('/login');
      //return;
    }
    // Load the wordpairs.
    // TODO: test should be a different set of data?
    $http.get('/data/wordpairs.json').then(loadWordPairs)
  };

  function loadWordPairs(response) {
    console.log('response.data='+response.data);
    $scope.numPairs = response.data.length;
    if ($scope.numPairs < 1) {
      // TODO: user visible error
      console.log("Loaded data only has " + $scope.numPairs + " elements");
      return;
    }

    $scope.wordpairs = response.data;
    $scope.curPair = 0;
  }

  $scope.submit = function() {
    if (!$scope.input) {
      $scope.error = "Please enter a word.";
      return;
    }
    $scope.error = "";
    $scope.input = ""
    $scope.wrong = true;
    $scope.curPair++;
    if ($scope.curPair >= $scope.wordpairs.length) {
      // loop
      $scope.curPair = 0;
    }
  };
}]);
