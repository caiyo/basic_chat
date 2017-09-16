(function(){
    'use strict';
    angular.module('main')
    .factory('AuthInterceptor', authInterceptorFunc);

    authInterceptorFunc.$inject=['$rootScope', '$window', '$q'];

    function authInterceptorFunc($rootScope, $window, $q){
        var interceptor = {
            request : requestInterceptor,
            response : responseInterceptor
        };

        return interceptor;

        function requestInterceptor(config){
            config.headers = config.headers || {};
            if ($window.localStorage.token){
                config.headers.Authorization = 'JWT ' + $window.sessionStorage.token;
            }

            return config;
        }

        function responseInterceptor(response){
            if (response.status === 401) {
                // handle the case where the user is not authenticated
            }
            return response || $q.when(response);
        }
    }

    angular.module('main').config(function ($httpProvider) {
        $httpProvider.interceptors.push('AuthInterceptor');
    });
})();