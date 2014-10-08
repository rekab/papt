module.exports = function(config){
  config.set({

    basePath : './',

    files : [
      'static/bower_components/angular/angular.js',
      'static/bower_components/angular-route/angular-route.js',
      'static/bower_components/angular-mocks/angular-mocks.js',
      'static/components/**/*.js',
      'static/view/**/*.js',
    ],

    autoWatch : true,

    frameworks: ['jasmine'],

    browsers : ['Chrome'],

    plugins : [
            'karma-chrome-launcher',
            'karma-firefox-launcher',
            'karma-jasmine',
            'karma-junit-reporter'
            ],

    junitReporter : {
      outputFile: 'test_out/unit.xml',
      suite: 'unit'
    }

  });
};
