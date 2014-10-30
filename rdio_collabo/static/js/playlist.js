$(document).ready(function(){
	var socket = io.connect('http://' + document.domain + ':' + location.port + '/playlist');
	socket.on('playlist connect response', function(result){
		console.log(result.message);

		// join room that is associated with the list id.
        socket.emit("join", {room: GetPlaylistID()});
	});

	// join room
	socket.on('room join response', view.UpdateJoined)

	// Song nomination
	$('#search-nominate').click(function(){
		$('#results').text('Loading...');
		var query = $('#query-nominate').val();
		var csrfToken = $('meta[name=csrf-token]').attr('content');
		backendHandler.SearchTracks(query, csrfToken, view.PrintSearchResults);
	});

	$('#song-nomination-form').submit(function(event){
	    // Stop submit from performing default actions.
	    event.preventDefault();

	    // Get Fields
	    var track = {};
	    var playlist = $('#share-code').text();
	    track['key'] = $('#song-nominate-list').children("dl").children('#key').text();
	    var csrfToken = $('meta[name=csrf-token]').attr('content');

	    backendHandler.AddTrackToPlaylist(playlist, track, csrfToken, socket);
  	});

	socket.on('add track to playlist response', view.UpdateAddTrackSuccess);

	// Helper Functions
	function GetPlaylistID(){
        // Get the list id from the pathname
        var pathElements = window.location.pathname.replace(/\/$/, '').split('/')
        return pathElements[pathElements.length - 1]
	}
});