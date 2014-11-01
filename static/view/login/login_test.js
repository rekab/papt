'use strict';

// Mock out papt.userservice.
angular.module('papt.userservice', []);

describe('papt.login module', function() {

  beforeEach(module('papt.userservice')); // Loads our flavor crystals.
  beforeEach(module('papt.login'));

  describe('login controller', function() {
    var mockScope, mockLocation, mockUserService;

    beforeEach(inject(function($rootScope, $location, $controller) {
      mockScope = $rootScope.$new();
      mockLocation = $location;
      mockUserService = {
        setUser: function(user) { this.user = user; }
      };
      var controller = $controller(
        'LoginCtrl',
        { 
          $scope: mockScope,
          $location: mockLocation,
          userService: mockUserService
        });
    }));

    it('should error when no user', inject(function() {
      mockScope.login();
      expect(mockScope.error).toBeTruthy();
    }));

    it('should succeed when there is a user', inject(function() {
      mockScope.userid = "foo";
      mockScope.login();
      expect(mockScope.error).not.toBeTruthy();
      expect(mockUserService.user).toBe("foo");
      expect(mockLocation.path()).toBe('/home');
    }));

  });
});
