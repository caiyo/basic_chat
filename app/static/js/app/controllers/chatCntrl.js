(function(){
    'use strict';
    angular.module('main')
    .controller('ChatCntrl', chatCntrl);

    chatCntrl.$inject = ['userservice', 'socketservice', '$scope', '$timeout'];

    function chatCntrl(userservice, socketservice, $scope, $timeout){
        var vm = this;
        vm.postMsg = postMsg;
        vm.currentUser = userservice.getCurrentUser();
        vm.newUnreadMessages = false;
        vm.scrollToBottom = scrollToBottom;
        vm.loadingMessages = false;
        vm.noNewMessages = false;

        socketservice.forward('new_message', $scope);
        socketservice.forward('socket_connected', $scope);
        socketservice.forward('new_group_member', $scope);

        $scope.$on('socket:new_message', socketNewMessageCallback);
        $scope.$on('socket:socket_connected', socketConnectCallback);
        $scope.$on('socket:new_group_member', socketNewGroupMemberCallback)

        var msgContainer = $('#msg-container');

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
                if (onLastMessage()){
                    scrollToBottom();
                }
                else{
                    vm.newUnreadMessages = true;
                }
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
            msgContainer.animate({ scrollTop: msgContainer.prop("scrollHeight")}, 500);
            vm.newUnreadMessages = false;
        }

        function onLastMessage(){
            if (!$('.chat-message').length){
                return true;
            }
            var lastMsg = $('.chat-message').last();
            if(msgContainer.scrollTop() + msgContainer.height() > msgContainer.prop('scrollHeight') - lastMsg.height()+10) {
                return true;
            }
            return false;
        }

        function loadOldMessages(firstMessage){
            vm.loadingMessages = true
            $timeout(function(){
                userservice.getOldMessages(vm.currentUser.user.activeGroup.id, firstMessage.msg_id, keepPosition());
            });

            function keepPosition(){
                var currentScrollTop = msgContainer.scrollTop();
                var currentScrollHeight =  msgContainer.prop('scrollHeight');
                var previousLocation = currentScrollHeight - currentScrollTop;

                return function(noNewMessages){
                    msgContainer.scrollTop(msgContainer.prop('scrollHeight') - previousLocation);
                    vm.loadingMessages = false;
                    if (noNewMessages){
                        vm.noNewMessages = true;
                        $timeout(function(){
                            vm.noNewMessages = false;
                        }, 1000);
                    }
                }
            }
        }

        $("#msg-container").scroll(function () {
            if(onLastMessage()){
                vm.newUnreadMessages = false;
                $scope.$apply();
            }
            if(vm.currentUser.user && $('#msg-container').scrollTop() === 0){
                var firstMessage = vm.currentUser.user.activeGroup.messages[0];
                if (firstMessage){
                    loadOldMessages(firstMessage);
                }
                console.log("at top");


            }
        });
    }
})();