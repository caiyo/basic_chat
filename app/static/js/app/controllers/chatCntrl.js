(function(){
    'use strict';
    angular.module('main')
    .controller('ChatCntrl', chatCntrl);

    chatCntrl.$inject = ['userservice'];

    function chatCntrl(userservice){
        var vm = this;



        vm.postMsg = postMsg;
        vm.getTimeStamp = getTimeStamp;
        vm.currentUser = userservice.getCurrentUser();

        function postMsg (e){
            e.preventDefault();
            if (!vm.msg){
                return;
            }

            userservice.postMessage(vm.msg).then(function(msg){
               vm.currentUser.user.activeGroup.messages.push(msg);
            }, function(r){
                console.log("error posting message", r);
            });

            vm.msg = null;
        }

        function getTimeStamp(timeString){
            return moment(timeString).format('MM/DD @ HH:MM')
        }
    }
})();