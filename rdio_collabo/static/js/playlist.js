$(document).ready(function(){
	var socket = io.connect('http://' + document.domain + ':' + location.port + '/playlist');
	socket.on('my response', function(msg){
		console.log(msg.data);
		view.Connected(); 
	});
});