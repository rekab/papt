'use strict';

// Declare app level module which depends on views, and components
angular.module('papt', [
  'ngRoute',
  'papt.login',
  'papt.instructions',
  'papt.wordpairs',
  'papt.testinstructions',
  'papt.test',
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/login'});
}]);
