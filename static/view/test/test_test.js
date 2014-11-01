'use strict';

describe('papt.test module', function() {

  beforeEach(module('papt.test'));

  describe('instructions controller', function() {
    var mockScope, mockLocation, mockHttp, fakeUserService, mockTestService;

    beforeEach(inject(function($rootScope, $location, $controller, $httpBackend) {
      mockScope = $rootScope.$new();
      mockLocation = $location;
      mockHttp = $httpBackend;
      mockTestService = {
        startTest: function(flavor) { this.flavor = flavor; }
      };
      var controller = $controller(
        'TestCtrl',
        { 
          userService: fakeUserService,
          testService: mockTestService,
          $scope: mockScope,
          $location: mockLocation,
          $http: $httpBackend
        });
    }));

    it('should redirect when no user', inject(function() {
      //mockScope.start();
      //expect(mockLocation.path()).toBe('/login');
    }));
  });
});
