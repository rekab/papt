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
    // TODO: summary report
  };

  $scope.showUserReport = function(username) {
    // TODO: should route to a view so the username is in the URL, with browser history
    $http.get('/report/view/' + username).then(
      function(response) {
        $scope.error = "";
        $scope.reportContent = $sce.trustAsHtml(response.data.report);
      },
      function(failureResponse) {
        $scope.error = failureResponse.data.error || "Server error";
        $scope.reportContent = "";
      });
  };
}]);
