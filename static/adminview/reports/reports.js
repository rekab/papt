'use strict';

angular.module('papt.reports', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/reports', {
    templateUrl: '/adminview/reports/reports.html',
    controller: 'ReportsCtrl'
  });
}])

.controller('ReportsCtrl', ['$scope', '$http', function($scope, $http) {
  $scope.error = "";
  $scope.users = [];

  $scope.getUserList = function() {
    $http.get('/report/list_users').then(
      function(response) {
        $scope.users = response.data.usernames;
      },
      function(failureResponse) {
        $scope.error = failureResponse.data.error || "Server error";
      });
  };


  $scope.showSummaryReport = function() {
  };

  $scope.showUserReport = function(username) {
  };
}]);
