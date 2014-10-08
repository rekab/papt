'use strict';

describe('papt.wordpairs module', function() {

  beforeEach(module('papt.wordpairs'));

  describe('wordpairs controller', function() {
    var mockScope, mockLocation, mockHttp, mockInterval;
    var wordpairDataHandler;

    beforeEach(inject(function($rootScope, $location, $httpBackend, $interval, $controller) {
      mockScope = $rootScope.$new();
      mockLocation = $location;
      mockInterval = $interval;
      mockHttp = $httpBackend;

      var controller = $controller(
        'WordpairsCtrl',
        { 
          $scope: mockScope,
          $location: mockLocation,
          $interval: mockInterval
        });
      wordpairDataHandler = mockHttp.when('GET', '/data/wordpairs.json')
        .respond([["foo", "bar"], ["qux", "baz"]]);
    }));

    afterEach(function() {
      mockHttp.verifyNoOutstandingExpectation();
      mockHttp.verifyNoOutstandingRequest();
    });

    it('should redirect when no user', inject(function() {
      mockScope.start();
      expect(mockLocation.path()).toBe('/login');
    }));

    it('should load word pairs and start the countdown', inject(function() {
      mockScope.userid = "foo";
      mockScope.start();
      mockHttp.flush();
      expect(mockLocation.path()).not.toBe('/login');
      expect(mockScope.wordpairs).toBeDefined();
      expect(mockScope.wordpairs[0][0]).toBe('foo')
      expect(mockScope.numPairs).toBe(2);
      expect(mockScope.curPair).toBe(0);
      expect(mockScope.numTicksLeft).toBe(300)

      // Time moves forward, expect the tick.
      mockInterval.flush(10);
      expect(mockScope.numTicksLeft).toBe(299)

      // Skip ahead to the last tick, expect curPair to change.
      mockScope.numTicksLeft = 1
      mockInterval.flush(10);
      expect(mockScope.curPair).toBe(1);

      // Skip ahead again, past the last pair, and expect the view to change.
      mockScope.numTicksLeft = 1
      mockInterval.flush(10);
      expect(mockLocation.path()).toBe('/testinstructions');
    }));
  });
});


