(function(){
    angular.module('main')
    .controller('ChatCntrl', chatCntrl);

    function chatCntrl(){
        var vm = this;
        vm.title = "Chat Controller!"
    }
})();