(function(){
    'use strict';
    angular.module('main')
    .factory('userservice', userService);

    userService.$inject = ['dataservice', '$window', '$q', 'socketservice'];

    function userService(dataservice, $window, $q, socketservice){
        var currentUser = {user : null};

        return {
            getCurrentUser : getCurrentUser,
            setCurrentUser : setCurrentUser,
            login: login,
            logout: logout,
            signup: signup,
            postMessage: postMessage,
            updateGroupViewed : updateGroupViewed,
            getLatestMessages : getLatestMessages
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
                    connectToGroupSockets(user.groups);
                }
            }
            else{
                if ($window.localStorage.token){
                    dataservice.getLoggedInUser()
                    .then(getLoggedInUserSuccess, function(){setCurrentUser(null);});
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
                    console.log('failure!', response);
                    return $q.reject(response);
                });
        }

        function logout(){
            dataservice.logout().then(function(){
                setCurrentUser(null);
                $window.localStorage.removeItem('token');
                socketservice.disconnect();
            });


        }

        function loginSuccess(data){

            $window.localStorage.token = data.access_token;
            return dataservice.getLoggedInUser().then(getLoggedInUserSuccess);
        }

        function loginFail(data){
            return $q.reject(response);
        }

        function getLoggedInUserSuccess(user){
            setCurrentUser(user);
            console.log('test');
            socketservice.connect();
            socketservice.emit('my event', {username : user.username});
        }

        function postMessage(msg, callback){
            var userid = currentUser.user ? currentUser.user.id : null;
            var groupid = userid ? currentUser.user.activeGroup.id : null

            if (!userid || ! groupid) return;

            return dataservice.postMessage(userid, groupid, msg);

            function postMessageSuccess (data){
                data.created_when = moment()
                data.username = currentUser.user.username;
                return data;

            }

            function postMessageFail(){

            }
        }

        function connectToGroupSockets(groups){
            if (!currentUser.user || !groups){
                return;
            }
            else{
                console.log("connecting");
                if (typeof groups === 'string'){
                    groups = [groups];
                }
                var groupIds = _.map(groups,
                                        function(o){return o.id;});
                socketservice.emit('join_room', {
                    groupIds: groupIds
                });
            }
        }

        function updateGroupViewed(groupid){
            return dataservice.updateGroupViewed(groupid);
        }

        function getLatestMessages(groupid){
            dataservice.getLatestMessages(groupid).then(function(msgs){
                if (msgs)
                    Array.prototype.push.apply(currentUser.user.activeGroup.messages, msgs);
            });
        }


    }
})();