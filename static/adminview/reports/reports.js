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
  $scope.reportContent = $sce.trustAsHtml("");
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
        $scope.categories = groupBy(response.data.answers, 'category');
        $scope.words = groupBy(response.data.answers, 'expected');
        $scope.summary = true;
      },
      function(failureResponse) {
        $scope.error = failureResponse.data.error || "Server error";
        $scope.reportContent = "";
        $scope.summary = false;
      });
  };

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

  $scope.showWordDrilldown = function(word) {
    $http.get('/report/drilldown/word/' + word).then(
      function(response) {
        $scope.error = "";
        $scope.drilldown = response.data.answers;
      },
      function(failureResponse) {
        $scope.error = failureResponse.data.error || "Server error";
        $scope.reportContent = "";
        $scope.summary = false;
      });
  }

  $scope.showCategoryDrilldown = function(category) {
    $http.get('/report/drilldown/category/' + category).then(
      function(response) {
        $scope.error = "";
        $scope.drilldown = response.data.answers;
      },
      function(failureResponse) {
        $scope.error = failureResponse.data.error || "Server error";
        $scope.reportContent = "";
        $scope.summary = false;
      });
  }

  $scope.resetDrilldown = function() {
    console.log('reset drilldown');
    $scope.drilldown = [];
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
