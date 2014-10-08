'use strict';

describe('papt.login module', function() {

  beforeEach(module('papt.login'));

  describe('login controller', function() {
    var mockRootScope, mockScope, mockLocation;

    beforeEach(inject(function($rootScope, $location, $controller) {
      mockRootScope = $rootScope.$new();
      mockScope = $rootScope.$new();
      mockLocation = $location;
      var controller = $controller(
        'LoginCtrl',
        { 
          $rootScope: mockRootScope,
          $scope: mockScope,
          $location: mockLocation
        });
    }));

    it('should error when no user', inject(function() {
      mockScope.login();
      expect(mockScope.error).toBeTruthy();
    }));

    it('should succeed when there is a user', inject(function() {
      mockScope.userid = "foo"
      mockScope.login();
      expect(mockScope.error).not.toBeTruthy();
      expect(mockLocation.path()).toBe('/instructions');
      expect(mockRootScope.userid).toBe("foo");
    }));

  });
});
