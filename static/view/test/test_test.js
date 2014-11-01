'use strict';

describe('papt.test module', function() {

  beforeEach(module('papt.test'));

  describe('instructions controller', function() {
    var mockScope, mockLocation, mockHttp, fakeUserService;

    beforeEach(inject(function($rootScope, $location, $controller, $httpBackend) {
      mockScope = $rootScope.$new();
      mockLocation = $location;
      mockHttp = $httpBackend;
      var controller = $controller(
        'TestCtrl',
        { 
          userService: fakeUserService,
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
