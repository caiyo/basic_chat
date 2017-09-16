(function(){
    'use strict'
    angular.module('main', ['ngRoute'])
    .config(['$interpolateProvider', function($interpolateProvider) {
      $interpolateProvider.startSymbol('{[');
      $interpolateProvider.endSymbol(']}');
    }])
    .config(function ($routeProvider, $locationProvider) {
        $locationProvider.hashPrefix('');
        $routeProvider
            .when('/', {
                templateUrl: '../../static/html/index.html',
                controller: 'ChatCntrl',
                controllerAs: 'chat',
            })
            .when('/login', {
                templateUrl: '../../static/html/login.html',
                controller: 'LoginCntrl',
                controllerAs: 'login',
                resolve : {
                    checkLoginStatus : checkLoginStatus
                }
            })
            .when('/signup', {
                templateUrl: '../../static/html/signup.html',
                controller: 'SignupCntrl',
                controllerAs: 'signup',
                resolve : {
                    checkLoginStatus : checkLoginStatus
                }
            });



    });

    function checkLoginStatus(userservice, $location){
        if (userservice.getCurrentUser().user){
            $location.path('/');
        }
    }
})();