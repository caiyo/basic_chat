(function(){
    'use strict'
    angular
    .module('main')
    .controller('AppController', appCntrl);

    appCntrl.$inject = ['$scope', '$location', 'userservice'];

    function appCntrl($scope, $location, userservice){
        var vm = this
        vm.text = "HELLO WORLD!";
        vm.logout = logout;

        vm.currentUser = userservice.getCurrentUser();

        userservice.setCurrentUser();

        function logout(){
            userservice.logout()
        }

        $scope.$on('$routeChangeSuccess', updateNavBarHighlight);

        function updateNavBarHighlight ($event){
            vm.currentTab = $location.path();
        }
    }
})();