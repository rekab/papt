'use strict';

angular.module('papt.reports', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/reports', {
    templateUrl: '/adminview/reports/reports.html',
    controller: 'ReportsCtrl'
  });
}])

.controller('ReportsCtrl', ['$scope', '$http', '$sce', function($scope, $http, $sce) {
  $scope.error = "";
  $scope.summary = false;
  $scope.summaryGrouping = "category";
  $scope.reportContent = $sce.trustAsHtml("<b>click stuff</b>");
  $scope.users = [];

  $scope.getUserList = function() {
    $http.get('/report/list_users').then(
      function(response) {
        $scope.error = "";
        $scope.users = response.data.usernames;
      },
      function(failureResponse) {
        $scope.error = failureResponse.data.error || "Server error";
      });
  };

  $scope.showSummaryReport = function() {
    $http.get('/report/get_summary').then(
      function(response) {
        $scope.error = "";
        $scope.reportContent = "";
        $scope.categories = groupByCategory(response.data.answers);
        $scope.words = groupByWord(response.data.answers);
        $scope.summary = true;
      },
      function(failureResponse) {
        $scope.error = failureResponse.data.error || "Server error";
        $scope.reportContent = "";
        $scope.summary = false;
      });
  };

  function groupByCategory(answers) {
    return groupBy(answers, 'category');
  }

  function groupByWord(answers) {
    return groupBy(answers, 'expected');
  }

  function groupBy(answers, key) {
    var groups = {};
    for (var i=0; i < answers.length; i++) {
      var answer = answers[i];

      if (!groups[answer[key]]) {
        groups[answer[key]] = {
          'correct': 0,
          'incorrect': 0
        };
      }

      if (answer.correct) {
        groups[answer[key]].correct++;
      } else {
        groups[answer[key]].incorrect++;
        console.log(answer[key] + ' is incorrect: ' + groups[answer[key]].incorrect)
      }
    }
    var ret = [];
    for (var group in groups) {
      var sum = {};
      sum.name = group;
      sum.correct = groups[group].correct;
      sum.incorrect = groups[group].incorrect;
      ret.push(sum);
    }
    return ret;
  }

  $scope.showUserReport = function(username) {
    // TODO: should route to a view so the username is in the URL, with browser history
    $http.get('/report/view/' + username).then(
      function(response) {
        $scope.error = "";
        $scope.summary = false;
        $scope.reportContent = $sce.trustAsHtml(response.data.report);
      },
      function(failureResponse) {
        $scope.error = failureResponse.data.error || "Server error";
        $scope.summary = false;
        $scope.reportContent = "";
      });
  };
}]);
