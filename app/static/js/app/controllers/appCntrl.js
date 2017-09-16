(function(){
    'use strict'
    angular
    .module('main')
    .controller('AppController', appCntrl);

    appCntrl.$inject = ['$scope', '$location', 'userservice'];

    function appCntrl($scope, $location, userservice){
        var vm = this
        vm.text = "HELLO WORLD!";
        vm.getCurrentUser = getCurrentUser;
        vm.getText = getText;
        vm.currentUser = null

        getCurrentUser();

        function getText(){
            return true;
        };
        function getCurrentUser (){
            return userservice.getCurrentUser().then(function(data){
                vm.currentUser = data;
            });
        }
        $scope.$on('$routeChangeSuccess', updateNavBarHighlight);

        function updateNavBarHighlight ($event){
            vm.currentTab = $location.path();
        }
    }
})();