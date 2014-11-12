'use strict';

// Declare app level module which depends on views, and components
angular.module('paptadmin', [
  'ngRoute',
  'papt.reports'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/reports'});
}]);
