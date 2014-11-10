'use strict';

// Fake the papt.userservice module dependency so we can mock it out.
angular.module('papt.userservice', []);

describe('papt.login module', function() {

  beforeEach(module('papt.userservice')); // Loads our fake version above.
  beforeEach(module('papt.login'));

  describe('login controller', function() {
    var mockScope, mockLocation, mockUserService, mockHttp;

    beforeEach(inject(function($rootScope, $location, $controller, $httpBackend) {
      mockScope = $rootScope.$new();
      mockLocation = $location;
      mockHttp = $httpBackend;
      mockUserService = {
        setUser: function(user, csrfToken) { 
          this.user = user; 
          this.csrfToken = csrfToken; 
        }
      };
      var controller = $controller(
        'LoginCtrl',
        { 
          $scope: mockScope,
          $location: mockLocation,
          userService: mockUserService
        });
    }));

    afterEach(function() {
      mockHttp.verifyNoOutstandingExpectation();
      mockHttp.verifyNoOutstandingRequest();
    });

    it('should error when no user', inject(function() {
      mockScope.login();
      expect(mockScope.error).toBeTruthy();
    }));

    it('should succeed when there is a user', inject(function() {
      mockScope.userid = "foo";
      mockHttp.expectGET("/user/login/foo").respond({
          "csrf_token": "some_string", 
          "error": null
      });

      mockScope.login();
      mockHttp.flush();

      expect(mockScope.error).not.toBeTruthy();
      expect(mockUserService.user).toBe("foo");
      expect(mockUserService.csrfToken).toBe("some_string");
      expect(mockLocation.path()).toBe('/home');
    }));


    it('should handle an angry server response', inject(function() {
      mockScope.userid = "foo";
      mockHttp.expectGET("/user/login/foo").respond(401, {
          "error": "say what"
      });

      mockScope.login();
      mockHttp.flush();
      expect(mockScope.error).toBe("say what");
      expect(mockUserService.user).not.toBe("foo");
      expect(mockLocation.path()).not.toBe('/home');
    }));

  });
});
