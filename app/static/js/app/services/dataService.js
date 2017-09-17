(function(){
    'use strict';
    angular
        .module('main')
        .factory('dataservice', dataservice);

    dataservice.$inject = ['$http', '$window', '$q', 'socketservice'];

    function dataservice($http, $window, $q, socketservice) {
        return {
            login: login,
            logout: logout,
            signup: signup,
            getLoggedInUser: getLoggedInUser,
            postMessage: postMessage,
            updateGroupViewed : updateGroupViewed,
            getLatestMessages : getLatestMessages
        };

        function login(username, password) {
            var parameters = JSON.stringify({'username': username, 'password': password});
            return $http.post('/auth', parameters)
                .then(getLoginComplete);

            function getLoginComplete(response) {
                return response.data;
            }

        }

        function logout(){
            return $http.post('/logout')
        }

        function signup(username, password, confirmPassword){
            var parameters = JSON.stringify({'username': username, 'password': password, 'confirmPassword': confirmPassword});
            return $http.post('/api/user', parameters)
                .then(getSignupComplete, getsignupFail)

            function getSignupComplete(response) {
                return login(username, password);
            }

            function getsignupFail(response){
                return $q.reject(response);
            }
        }

        function getLoggedInUser(){
            return $http.get('/api/user').then(getUserSucess, getUserFail);

            function getUserSucess(response){
                return response.data
            }

            function getUserFail(response){
                return $q.reject(response);
            }
        }

        function postMessage(userid, groupid, msg){
            var parameters = {'groupid': groupid, 'message' : msg};
            socketservice.emit('post_message', parameters)
        }

        function updateGroupViewed(groupid){
            return $http.post('/api/chatgroup/'+groupid+'/messages/viewed');

        }

        function getLatestMessages(groupid){
            return $http.get('/api/chatgroup/'+groupid+'/messages/latest')
                       .then(function(result){
                            return result.data;
                       });
        }
    }
})();
