var socket = io.connect('http://127.0.0.1:5000/');

socket.on('connect', function () {
    socket.send('I am now connected');

    socket.emit('custom event', 'The custom event message');

    socket.on('from flask', function (msg) {
       alert(msg);
    });

    socket.on('message', function (msg) {
        alert(msg);
    });
});