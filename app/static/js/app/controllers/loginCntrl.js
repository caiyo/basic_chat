(function(){
    angular.module('main')
    .controller('LoginCntrl', loginCntrl);

    loginCntrl.$inject = ['dataservice', '$window', '$location'];

    function loginCntrl(dataservice, $window, $location){
        var vm = this;
        vm.submitLogin = submitLogin;
        vm.errors = [];

        function submitLogin(event){
            vm.errors = [];
            event.preventDefault();
            dataservice.login(vm.username, vm.password)
                .then(successLogin)
                 .catch(failLogin);
        }

        function successLogin(data){
            console.log("success!!", data);
            //Session is only alive as long as the tab stays open

            $location.path('/');
        }

        function failLogin(results){
            vm.errors.push('Incorrect username or password');
        }
    }
})();