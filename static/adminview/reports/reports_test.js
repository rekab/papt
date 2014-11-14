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

    it('should call the server to get a report', function() {
      mockScope.error = 'some old error message';
      mockHttp.expectGET('/report/view/someuser').respond(200, {'report': 'stuff'});
      mockScope.showUserReport('someuser');
      mockHttp.flush();
      expect(mockScope.error).toBe('');
      expect(mockScope.reportContent).toBeTruthy();
    });

    it('should display an error if the report call fails', function() {
      mockScope.reportContent = 'some old report content';
      mockHttp.expectGET('/report/view/someuser').respond(400, {'error': 'broken'});
      mockScope.showUserReport('someuser');
      mockHttp.flush();
      expect(mockScope.error).toBe('broken');
      expect(mockScope.reportContent).not.toBeTruthy();
    });

  });
});
