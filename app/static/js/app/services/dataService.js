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
            getLatestMessages : getLatestMessages,
            getMessages : getMessages
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
                console.log("succes signup");
                return login(username, password);
            }

            function getsignupFail(response){
                console.log("fail signup", response);
                return $q.reject(response);
            }
        }

        function getLoggedInUser(){
            return $http.get('/api/user').then(getUserSucess, getUserFail);

            function getUserSucess(response){
                if (response.data && response.data.user){
                    return response.data.user;
                }
                else{
                    return $q.reject(response);
                }
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

        function getMessages(groupid, beforeMessageId){
            var params = beforeMessageId ? {beforemsgid : beforeMessageId} : null;
            return $http.get('/api/chatgroup/'+groupid+'/messages', {'params': params})
                       .then(function(result){
                            return result.data;
                       });
        }
    }
})();
