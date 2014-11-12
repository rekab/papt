'use strict';

angular.module('papt.reports', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/reports', {
    templateUrl: 'adminview/reports/reports.html',
    controller: 'ReportsCtrl'
  });
}])

.controller('ReportsCtrl', ['$scope', function($scope) {
  $scope.getReportList = function() {
  };
  $scope.getReportSummary = function() {
  };
  $scope.getReport = function() {
  };
}]);
