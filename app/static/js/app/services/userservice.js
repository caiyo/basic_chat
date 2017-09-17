(function(){
    'use strict';
    angular.module('main')
    .factory('userservice', userService);

    userService.$inject = ['dataservice', '$window', '$q'];

    function userService(dataservice, $window, $q){
        var currentUser = {user : null};

        return {
            getCurrentUser : getCurrentUser,
            setCurrentUser : setCurrentUser,
            login: login,
            logout: logout,
            signup: signup,
            postMessage: postMessage,
        };

        function getCurrentUser(){
            return currentUser;
        }

        function setCurrentUser(user){
            if (user || user === null){
                console.log(user);
                currentUser.user = user;
                if (currentUser.user){

                    currentUser.user.activeGroup = user.groups && user.groups.length ? user.groups[0] : null;
                }
            }
            else{
                if ($window.localStorage.token){
                    dataservice.getLoggedInUser().then(function(user){
                        setCurrentUser(user);
                    }, function(){setCurrentUser(null)});
                }

            }

        }

        function login(username, password){
            return dataservice.login(username, password).then(loginSuccess, loginFail);
        }

        function signup(username, password, confirmPassword){
            return dataservice.signup(username, password, confirmPassword)
                .then(function(response){
                    login(username, password);
                }, function(response){
                    $q.reject(reponse);
                });
        }

        function logout(){
            setCurrentUser(null);
            $window.localStorage.removeItem('token');
        }

        function loginSuccess(data){

            $window.localStorage.token = data.access_token;
            return dataservice.getLoggedInUser().then(function(user){
                setCurrentUser(user);
            });
        }

        function loginFail(data){
            return $q.reject(response);
        }

        function postMessage(msg){
            var userid = currentUser.user ? currentUser.user.id : null;
            var groupid = userid ? currentUser.user.activeGroup.id : null

            if (!userid || ! groupid) return;

            return dataservice.postMessage(userid, groupid, msg).then(postMessageSuccess, postMessageFail);

            function postMessageSuccess (data){
                data.created_when = moment()
                data.username = currentUser.user.username;
                return data;

            }

            function postMessageFail(){

            }
        }
    }
})();