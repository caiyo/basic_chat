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
            controllerAs: 'vm',
            bindToController: true
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