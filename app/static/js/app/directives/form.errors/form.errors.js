(function(){
    angular.module('main')
    .directive('formErrors', formErrors);

    function formErrors(){
        var directive = {
            link : link,
            templateUrl: '../../static/js/app/directives/form.errors/form.errors.html',
            restrict: 'EA',
            scope: {
                errors : '='
            },
            controller: formErrorController,
            // note: This would be 'ExampleController' (the exported controller name, as string)
            // if referring to a defined controller in its separate file.
            controllerAs: 'vm',
            bindToController: true // because the scope is isolated
        };

        return directive;

        function link(scope, element, attrs, vm){

        }

    }

    formErrorController.$inject = ['$scope'];

    function formErrorController($scope){
        var vm = this;


    }
})();