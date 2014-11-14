'use strict';

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

    it('should call the server to get users', function() {
      var users = ['foo', 'bar'];
      mockHttp.expectGET('/report/list_users').respond(200, {'usernames': users});
      mockScope.getUserList();
      mockHttp.flush();
      expect(mockScope.users).toEqual(users);
    });

    it('should display an error if the get user call fails', function() {
      mockHttp.expectGET('/report/list_users').respond(400, {'error': 'broken'});
      mockScope.getUserList();
      mockHttp.flush();
      expect(mockScope.error).toBe('broken');
    });
  });
});
