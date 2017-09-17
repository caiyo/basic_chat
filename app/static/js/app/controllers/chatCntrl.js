(function(){
    'use strict';
    angular.module('main')
    .controller('ChatCntrl', chatCntrl);

    chatCntrl.$inject = ['userservice', 'socketservice', '$scope'];

    function chatCntrl(userservice, socketservice, $scope){
        var vm = this;



        vm.postMsg = postMsg;
        vm.getTimeStamp = getTimeStamp;
        vm.currentUser = userservice.getCurrentUser();

        socketservice.forward('new_message', $scope);
        socketservice.forward('socket_connected', $scope);

        $scope.$on('socket:new_message', function(event, data){
            if(vm.currentUser.user.activeGroup.id === data.group_id){
                vm.currentUser.user.activeGroup.messages.push(data);
                userservice.updateGroupViewed(data.group_id);
            }
        });

        $scope.$on('socket:socket_connected', function(event, data){
            console.log("youre connected!");
            userservice.getLatestMessages(vm.currentUser.user.activeGroup.id);
        });

        function postMsg (e){
            e.preventDefault();
            if (!vm.msg){
                return;
            }

            userservice.postMessage(vm.msg)

            vm.msg = null;
        }

        function getTimeStamp(timeString){
            return moment(timeString).format('MM/DD @ HH:MM')
        }
    }
})();