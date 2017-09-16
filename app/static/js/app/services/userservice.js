(function(){
    'use strict';
    angular.module('main')
    .factory('userservice', userService);

    userService.$inject = ['dataservice'];

    function userService(dataservice){
        var currentUser = null;

        return {
            getCurrentUser : getCurrentUser
        };

        function getCurrentUser(){
            if (!currentUser){
                return dataservice.getLoggedInUser().then(function(data){
                    currentUser = data;
                }, function(response){
                    currentUser = null;
                }).then(function(){console.log(currentUser); return currentUser});
            }
            else{
                return $q.resolve(currentUser);
            }
        }
    }
})();