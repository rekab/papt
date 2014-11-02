'use strict';

// Mock out papt.userservice.
angular.module('papt.userservice', []);

describe('papt.wordpairs module', function() {

  beforeEach(module('papt.userservice')); // Loads our flavor crystals.
  beforeEach(module('papt.wordpairs'));

  describe('wordpairs controller', function() {
    var mockScope, mockLocation, mockHttp, mockInterval, mockTimeout, mockUserService, fakeWordpairService;
    var wordpairDataHandler;

    beforeEach(inject(function($rootScope, $location, $httpBackend, $interval, $timeout, $controller) {
      mockScope = $rootScope.$new();
      mockLocation = $location;
      mockInterval = $interval;
      mockTimeout = $timeout;
      mockHttp = $httpBackend;
      mockUserService = {
        checkLoggedIn: function() { this.called = true; return true; }
      };
      fakeWordpairService = {
        // Should always fetch "wordpairs-a.json".
        getFlavor: function() { return 'a'; }
      };

      mockScope.beep = {
        playPause: function() { this.played = true; }
      };

      var controller = $controller(
        'WordpairsCtrl',
        { 
          $scope: mockScope,
          $location: mockLocation,
          $interval: mockInterval,
          $timeout: mockTimeout,
          userService: mockUserService,
          wordpairService: fakeWordpairService
        });
      wordpairDataHandler = mockHttp.when('GET', '/data/wordpairs-a.json')
        .respond([["foo", "bar"], ["qux", "baz"]]);
    }));

    afterEach(function() {
      mockHttp.verifyNoOutstandingExpectation();
      mockHttp.verifyNoOutstandingRequest();
    });

    it('should load word pairs and start the countdown', inject(function() {
      expect(mockUserService.called).not.toBeTruthy();
      mockScope.start();
      mockHttp.flush();
      expect(mockUserService.called).toBeTruthy();
      expect(mockLocation.path()).not.toBe('/login');
      expect(mockScope.wordpairs).toBeDefined();
      expect(mockScope.wordpairs[0][0]).toBe('foo')
      expect(mockScope.numPairs).toBe(2);
      expect(mockScope.curPair).toBe(0);
      expect(mockScope.numTicksLeft).toBe(300)

      // Time moves forward, expect the tick.
      mockInterval.flush(10);
      expect(mockScope.numTicksLeft).toBe(299)

      // Skip ahead to the last tick and send time forward.
      mockScope.numTicksLeft = 1
      mockInterval.flush(10);
      // Expect the beep to have been played.
      expect(mockScope.beep.played).toBeTruthy();
      // Skip ahead some more time for the sound to play.
      mockTimeout.flush(1000);
      expect(mockScope.curPair).toBe(1);

      // Reset the mock sound.
      mockScope.beep.played = false;

      // Skip ahead again, past the last pair, and expect the view to change.
      mockScope.numTicksLeft = 1
      mockInterval.flush(10);
      // Expect the beep to have been played.
      expect(mockScope.beep.played).toBeTruthy();
      // Skip ahead some more time for the sound to play.
      mockTimeout.flush(1000);
      expect(mockLocation.path()).toBe('/done');
    }));
  });
});


