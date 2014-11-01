'use strict';

angular.module('papt.test', ['ngRoute', 'papt.userservice'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/test', {
    templateUrl: 'view/test/test.html',
    controller: 'TestCtrl'
  });
}])

.factory('testService', ['$location', function($location) {
  var flavor;
  return {
    setFlavor: function(desiredFlavor) { flavor = desiredFlavor; },
    getFlavor: function() { return flavor; },
    goToTest: function(flavor) {
      console.log('Setting test flavor to ' + flavor + ' and redirecting to /test');
      this.setFlavor(flavor);
      $location.path('/test');
    }
  };
}])

.controller('TestCtrl', ['userService', 'testService', '$scope', '$location', '$http', function(userService, testService, $scope, $location, $http) {
  $scope.start = function() {
    if (!userService.checkLoggedIn()) {
      return;
    }
    // Load the test.
    var jsonPath = '/data/test-' + testService.getFlavor() + '.json';
    $http.get(jsonPath).then(loadTest, function() { alert('Failed to load test data :('); });
  };

  function loadTest(response) {
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
      $location.path('/home');
    }
  };
}]);
