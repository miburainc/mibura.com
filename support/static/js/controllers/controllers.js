angular
	.module("main-app.controllers")
	.controller("DashboardController", [ '$scope', '$http', '$location', function($scope, $http, $location) {

	  var _selected;
	  $scope.items = [];
	  $scope.cloudsupports = [];
	  $scope.process = {};
	  $scope.clouds = [];
	  $scope.cloudlist = { fields: {} };
	  $scope.quantities = {};
	  $scope.progress = 0;
	  $scope.total_cost = 0.00;


	  $scope.ngModelOptionsSelected = function(value) {
	    if (arguments.length) {
	      _selected = value;
	    } else {
	      return _selected;
	    }
	  };

	  $scope.modelOptions = {
	    debounce: {
	      default: 500,
	      blur: 250
	    },
	    getterSetter: true
	  };

	  $scope.getProduct = function(val) {
	    return $http.get('/support/api/productcomplete/', {
	      params: {
	        format: 'json',
	        s: val
	      }
	    }).then(function(response){
	      return response.data.results.map(function(item){
	        // return item.brand + ' | ' + item.model + ' | ' + item.category.name;
	        return item;
	      });
	    });
	  };


	  $scope.addProduct = function() {

	  	$scope.temp['serial'] = $scope.process.serial;
	  	$scope.items.push($scope.temp);
	    $scope.process.selected = '';	
	    $scope.process.serial = '';


	  };

	  $scope.onSelect = function ($item, $model, $label) {
	  	  $scope.temp = $item;
	      // $scope.items.push($item);
	      console.log($item);
	  };

	  $scope.delete = function (index) {
		$scope.items.splice(index, 1);
	  };


	  $scope.init = function() {

	  	$http.get('/support/api/cloud/')
		.then(function(response) {
	  		$scope.clouds = response.data.results;

	  	});

	  };

	  $scope.init();


	  $scope.addCloud = function(model) {
	  	console.log(model);
	  	$scope.cloudsupports.push(model);
	  };


	  $scope.step = function(i) {
	  	$scope.progress = i;
	  };

	  $scope.plans = function(plan) {
	  	var total = 0;
	  	if (array) {
	  	    angular.forEach(array, function(item) {
	  	        total += item['price_' + plan];
	  	    });
	  	}
	  	$scope.total_cost = total;
	  	
	  };



	   $scope.$watchCollection('items', function(array) {
	       var total = 0;
	       if (array) {
	           angular.forEach(array, function(item) {
	               total += item['price_silver'];
	           });
	       }
	       $scope.total_cost = total;
	   });



}]);