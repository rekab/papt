'use strict';

describe('papt.instructions module', function() {

  beforeEach(module('papt.instructions'));

  describe('instructions controller', function() {
    var mockScope, mockLocation;

    beforeEach(inject(function($rootScope, $location, $controller) {
      mockScope = $rootScope.$new();
      mockLocation = $location;
      var controller = $controller(
        'InstructionsCtrl',
        { 
          $scope: mockScope,
          $location: mockLocation
        });
    }));

    it('should redirect when no user', inject(function() {
      mockScope.checkLoggedIn();
      expect(mockLocation.path()).toBe('/login');
    }));

    it('should proceed on proceed()', inject(function() {
      mockScope.userid = "foo";
      mockScope.checkLoggedIn();
      expect(mockLocation.path()).not.toBe('/login');
      mockScope.proceed();
      expect(mockLocation.path()).toBe('/wordpairs');
    }));
  });
});
