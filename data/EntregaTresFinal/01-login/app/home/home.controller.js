(function () {

  'use strict';

  angular
    .module('app')
    .controller('HomeController', homeController);

  homeController.$inject = ['authService'];

  function homeController(authService) {

    var vm = this;
    vm.auth = authService;


  }
  function fun(){
console.log('Hola');
  	//$http.get('http://127.0.0.1:5000/alertas', config).then(function(response){
  	//	$scope.myData = response.data.records; 
//
  	//});


  }


})();