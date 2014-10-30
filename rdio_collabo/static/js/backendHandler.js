$(document).ready(function(){
  backendHandler = {
    CreatePlaylist: function(name, description, csrfToken, viewFunction){
      $.post('/playlists/create', 
        {'name': name,
         'description': description,
         'csrf_token': csrfToken },
          function(data){
            if('ok' === data['status'])
            { 
              // format data for view function.
              var result = data['result'];
              viewFunction(result);
            }
        }
      );
    },

    SearchTracks: function(query, csrfToken, viewFunction){
      $.post("/search/tracks", 
        {
          'query': query,
          'csrf_token': csrfToken
        },
        function(data){
          if('ok' === data['status'])
          {
            // format data for view function.
            var result = data['result']['results'];
            viewFunction(result);
          }
        });
    },

    // SearchPlaylists: function(query, csrfToken, viewFunction){
    //   $.post('/search/playlists', 
    //     {
    //       'query': query, 
    //       'csrf_token': csrfToken
    //     }, 
    //     function(data){
    //       if('ok' === data['status'])
    //       {
    //         // format data for view function
    //         console.log(data);
    //         //viewFunction();
    //       }
    //   });
    // },

    AddTrackToPlaylist: function(playlistKey, track, csrfToken, socket){
      socket.emit('add track to playlist', 
        {
          playlist_id: playlistKey,
          track_rdioID: track['key'],
          csrf_token: csrfToken
        });
    },
  };
});
