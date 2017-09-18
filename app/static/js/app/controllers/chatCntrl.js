(function(){
    'use strict';
    angular.module('main')
    .controller('ChatCntrl', chatCntrl);

    chatCntrl.$inject = ['userservice', 'socketservice', '$scope'];

    function chatCntrl(userservice, socketservice, $scope){
        var vm = this;
        vm.postMsg = postMsg;
        vm.currentUser = userservice.getCurrentUser();

        socketservice.forward('new_message', $scope);
        socketservice.forward('socket_connected', $scope);
        socketservice.forward('new_group_member', $scope);

        $scope.$on('socket:new_message', socketNewMessageCallback);
        $scope.$on('socket:socket_connected', socketConnectCallback);
        $scope.$on('socket:new_group_member', socketNewGroupMemberCallback)

        function postMsg (e){
            e.preventDefault();
            if (!vm.msg){
                return;
            }

            userservice.postMessage(vm.msg)
            scrollToBottom();
            vm.msg = null;
        }

        function socketConnectCallback(event, data){
            console.log("youre connected!");
            userservice.getLatestMessages(vm.currentUser.user.activeGroup.id);
            scrollToBottom();
        }

        function socketNewMessageCallback(event, data){
            if(vm.currentUser.user.activeGroup.id === data.group_id){
                vm.currentUser.user.activeGroup.messages.push(data);
                userservice.updateGroupViewed(data.group_id);
            }
        }

        function socketNewGroupMemberCallback(event, data){
            console.log("new gorup member");
            var group = _.find(vm.currentUser.user.groups,
                                function(o){
                                    return o.id === data.group_id
                                });
            if (group){
                group.members.push(data.user);
            }
        }

        function scrollToBottom(){
            $("#msg-container").animate({ scrollTop: $('#msg-container').prop("scrollHeight")}, 500);
        }

    }
})();