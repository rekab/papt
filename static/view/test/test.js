'use strict';

angular.module('papt.test', ['ngRoute', 'papt.userservice'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/test', {
    templateUrl: 'view/test/test.html',
    controller: 'TestCtrl'
  });
}])

.factory('testService', ['$location', function($location) {
  // TODO: this service is just strange/hacky, use $routeParams instead.
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

.controller('TestCtrl', [
    'userService', 'testService', '$scope', '$location', '$http', 
    function(userService, testService, $scope, $location, $http) {
  $scope.testFlavor = '';
  $scope.start = function() {
    if (!userService.checkLoggedIn()) {
      return;
    }
    $scope.testFlavor = testService.getFlavor();
    // Load the test.
    var jsonPath = '/data/test-' + testService.getFlavor() + '.json';
    $http.get(jsonPath).then(loadTest, function() { alert('Failed to load test data :('); });
  };

  function loadTest(response) {
    console.log('loaded test, response.data='+response.data);
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
    var pair = $scope.wordpairs[$scope.curPair];
    var postData = {
      username: userService.getUser(),
      csrf_token: userService.getCsrfToken(),
      expected: pair[1],
      answer: $scope.input,
      test_flavor: $scope.testFlavor
    };
    $http.post('/test/answer', postData).then(
        function(response) {
          $scope.error = "";
          $scope.input = ""
          $scope.curPair++;
          if ($scope.curPair >= $scope.wordpairs.length) {
            console.log('out of word pairs, redirecting to /done');
            $location.path('/done');
          }
        },
        function(failureResponse) {
          console.log('server error error: ' + failureResponse.status);
          $scope.error = failureResponse.data.error || "Server error";
        });
  };
}]);
