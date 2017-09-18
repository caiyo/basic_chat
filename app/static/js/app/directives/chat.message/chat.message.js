(function(){
    angular.module('main')
    .directive('chatMessage', chatMessage);

    function chatMessage(){
        var directive = {
            link : link,
            templateUrl: '../../static/js/app/directives/chat.message/chat.message.html',
            restrict: 'EA',
            scope: {
                message : '='
            },
            controller: chatMessageController,
            controllerAs: 'vm',
            bindToController: true
        };

        return directive;

        function link(scope, element, attrs, vm){
        }

    }

    chatMessageController.$inject = ['$scope'];

    function chatMessageController($scope){
        var vm = this;
        vm.getTimeStamp=getTimeStamp;

        function getTimeStamp(timeString){
            return moment(timeString).format('HH:mm MM/DD')
        }
    }
})();