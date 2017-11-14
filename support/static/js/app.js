// Angular App Starter
(function() {
  window.App = window.App || {};

  angular.module("main-app.controllers", []);
  angular.module("main-app.directives", []);
  var app = angular.module("main-app", ['main-app.controllers', 'main-app.directives', 'ngRoute', 'ui.bootstrap']);
  app.config(function ($interpolateProvider, $httpProvider) {
      $interpolateProvider.startSymbol('[[').endSymbol(']]');
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  })


  // Application Routes
  app.config(['$routeProvider',
      function($routeProvider) {
        $routeProvider.
            when('/', {
              templateUrl: static_url + 'html/home-checkout.html',
              controller: 'DashboardController'
            }).
          
            otherwise({
                redirectTo: '/'
            });
      }]
  );

  // Filters App
  app.filter('underscoreless', function() {
    return function (input) {
      return input.replace(/_/g, ' ');
    };
  });

  // Directives
  app.directive('toggle', function() {
      return {
        restrict: 'A',
        link: function(scope, element, attrs){
          if (attrs.toggle=="tooltip"){
            $(element).tooltip();
          }
          if (attrs.toggle=="popover"){
            $(element).popover();
          }
        }
      };
  });

})();
