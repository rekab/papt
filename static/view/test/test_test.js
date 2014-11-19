'use strict';

describe('papt.test module', function() {

  beforeEach(module('papt.test'));

  describe('instructions controller', function() {
    var mockScope, mockLocation, mockHttp, mockUserService, mockTestService;
    var testFlavor, loggedIn, userName, csrfToken;

    beforeEach(inject(function($rootScope, $location, $controller, $httpBackend) {
      mockScope = $rootScope.$new();
      mockLocation = $location;
      mockHttp = $httpBackend;
      mockTestService = {
        getFlavor: function() {
          return testFlavor;
        }
      };
      mockUserService = {
        getUser: function() {
          return userName;
        },
        getCsrfToken: function() {
          return csrfToken;
        },
        checkLoggedIn: function() {
          return loggedIn;
        }
      };
      var controller = $controller(
        'TestCtrl',
        { 
          userService: mockUserService,
          testService: mockTestService,
          $scope: mockScope,
          $location: mockLocation
        });
    }));

    afterEach(function() {
      mockHttp.verifyNoOutstandingExpectation();
      mockHttp.verifyNoOutstandingRequest();
    });

    it('should return when no user', function() {
      loggedIn = false;
      mockScope.start();
    });

    describe('started controller', function() {
      beforeEach(function() {
        loggedIn = true;
        testFlavor = 'foo';
        userName = 'user';
        mockScope.start();
        expect(mockScope.ready).not.toBeTruthy();
        mockHttp.expectGET('/data/test-foo.json').respond(200, [['foo', 'bar']]);
        mockHttp.expectPOST('/test/start', {
          username: userName,
          csrf_token: csrfToken,
          test_flavor: testFlavor}).respond(200, [['foo', 'bar']]);
        mockHttp.flush();
        expect(mockScope.curPair).toBe(0);
        expect(mockScope.ready).toBeTruthy();
      });


      it('should increment the counter after an answer, then redirect to /done', function() {
        mockScope.numPairs = 1;
        mockScope.input = 'answer';
        mockScope.submit()
        mockHttp.expectPOST('/test/answer', {
          username: userName,
          csrf_token: csrfToken,
          expected: 'bar',
          answer: 'answer',
          test_flavor: testFlavor}).respond(200, {message: 'ok', done: false});

        // Then the test should be finished.
        mockHttp.expectPOST('/test/finish', {
          username: userName,
          csrf_token: csrfToken,
          test_flavor: testFlavor}).respond(200, {message: 'ok'});
        mockHttp.flush();

        // Verify.
        expect(mockScope.curPair).toBe(1);
        expect(mockScope.ready).not.toBeTruthy()
        expect(mockLocation.path()).toBe('/done');
      });

      it('should handle empty input', function() {
        mockScope.input = '';
        mockScope.submit()
        expect(mockScope.error).toBe('Please enter a word.');
      });

      it('should handle a server error message', function() {
        mockScope.input = 'answer';
        mockScope.submit()
        mockHttp.expectPOST('/test/answer', {
          username: userName,
          csrf_token: csrfToken,
          expected: 'bar',
          answer: 'answer',
          test_flavor: testFlavor}).respond(400, {error: 'what'});
        mockHttp.flush();

        expect(mockScope.error).toBe('what');
        expect(mockScope.curPair).toBe(0);
      });
    });
  });
});
