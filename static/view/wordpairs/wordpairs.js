'use strict';

var WORDPAIR_DURATION_SECS = 3;

angular.module('papt.wordpairs', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/wordpairs', {
    templateUrl: 'view/wordpairs/wordpairs.html',
    controller: 'WordpairsCtrl'
  });
}])

.controller('WordpairsCtrl', 
    ['$scope', '$location', '$http', '$interval', '$window',
    function($scope, $location, $http, $interval, $window) {
  $scope.start = function() {
    // Check if the user is logged in.
    // TODO: move this repeated code somewhere common. Possibly as a service?
    if (!$scope.userid) {
      console.log("Not logged in");
      $location.path('/login');
      return;
    }
    // Load the wordpairs.
    $http.get('/data/wordpairs.json').then(loadWordPairs)
    /*.error(function() {
      // TODO: user visible error
    })*/;
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
    startCountdown();
  }

  function startCountdown() {
    $scope.maxNumTicks = 100 * WORDPAIR_DURATION_SECS;
    $scope.numTicksLeft = $scope.maxNumTicks;
    setTimeLeft();
    $scope.intervalPromise = $interval(countdown, 10, $scope.numTicksLeft);
    // Cancel the interval on navigation.
    $scope.$on("$destroy", function() {
      console.log('canceling interval');
      $interval.cancel($scope.intervalPromise);
    });
  }

  function setTimeLeft() {
    var secondsLeft = Math.ceil($scope.numTicksLeft / 100);
    var secondsInMinuteLeft = secondsLeft % 60;
    if (secondsInMinuteLeft < 10) {
      secondsInMinuteLeft = "0" + secondsInMinuteLeft;
    }
    $scope.timeLeft = Math.floor(secondsLeft / 60) + ":" + secondsInMinuteLeft;
  }

  function countdown() {
    $scope.numTicksLeft--;
    setTimeLeft();
    if ($scope.numTicksLeft == 0) {
      console.log('countdown over');
      showNextWordPair();
      return;
    }
    var width = (100 * ($scope.numTicksLeft / $scope.maxNumTicks));
    $scope.progressbarStyle = {width: width + "%"};
  }

  function showNextWordPair() {
    if ($scope.curPair == $scope.wordpairs.length - 1) {
      console.log('out of word pairs, redirecting to /testinstructions');
      $location.path('/testinstructions');
      return;
    }
    $scope.curPair++;
    startCountdown();
  }
}]);


