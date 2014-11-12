'use strict';

// Fake the papt.userservice module dependency so we can mock it out.
angular.module('papt.reports', []);

describe('papt.reports module', function() {

  beforeEach(module('papt.reports'));

  describe('reports controller', function() {
    var mockScope, mockHttp;

    beforeEach(inject(function($rootScope, $controller, $httpBackend) {
      mockScope = $rootScope.$new();
      mockHttp = $httpBackend;
      var controller = $controller(
        'ReportsCtrl',
        { 
          $scope: mockScope,
        });
    }));

    afterEach(function() {
      mockHttp.verifyNoOutstandingExpectation();
      mockHttp.verifyNoOutstandingRequest();
    });

  });
});
