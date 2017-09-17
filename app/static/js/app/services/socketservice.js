(function(){
    'use strict';
    angular
        .module('main')
        .factory('socketservice', socketservice);

    socketservice.$inject = ['socketFactory'];

    function socketservice(socketFactory) {
        var myIoSocket = io.connect('http://127.0.0.1:5000/',{
            reconnect: true
        });
        var mySocket = socketFactory({
            ioSocket: myIoSocket
        });
        mySocket.disconnect();

        return mySocket;
    }
})();
