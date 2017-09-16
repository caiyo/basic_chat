(function(){
    angular
        .module('main')
        .factory('dataservice', dataservice);

    dataservice.$inject = ['$http', '$window', '$q'];

    function dataservice($http, $window, $q) {
        return {
            login: login,
            signup: signup,
            getLoggedInUser: getLoggedInUser
        };

        function login(username, password) {
            var parameters = JSON.stringify({'username': username, 'password': password});
            return $http.post('/auth', parameters)
                .then(getLoginComplete);

            function getLoginComplete(response) {
                return response.data;
            }

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
    }
})();
