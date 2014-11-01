'use strict';

// Declare app level module which depends on views, and components
angular.module('papt', [
  'ngRoute',
  'mediaPlayer',
  'papt.login',
  'papt.home',
  'papt.instructions',
  'papt.wordpairs',
  'papt.testinstructions',
  'papt.test',
  'papt.userservice'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/login'});
}]);
