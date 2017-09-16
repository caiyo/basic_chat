(function(){
    'use strict';
    angular.module('main')
    .controller('SignupCntrl', signupCntrl);

    signupCntrl.$inject = ['dataservice', '$location'];
    function signupCntrl(dataservice, $location){
        var vm = this;
        vm.errors = [];
        vm.submitSignup = submitSignup;

        function submitSignup(event){

            vm.errors = [];
            event.preventDefault();

            if (vm.password != vm.confirmPassword){
                vm.errors.push("Password and confirm password don't match");
                return;
            }
            dataservice.signup(vm.username, vm.password, vm.confirmPassword)
                .then(successSignup, failSignup);
        }

        function successSignup(data){
            console.log("success!!", data);
            $location.path('/');
        }

        function failSignup(data){
            console.log(data)
            vm.errors.push(data.data);
        }
    }
})();