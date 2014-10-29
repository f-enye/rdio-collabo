$(document).ready(function() {
  // $("#search-playlists").submit(function(event){
  //   event.preventDefault();

  //   var playlistQuery = $("#search-playlists-query").val();
  //   var csrfToken = $('meta[name=csrf-token]').attr('content');

  //   backendHandler.SearchPlaylists(playlistQuery, csrfToken, view.ShowSearchResults);
  // });

  $('#create-playlist').submit(function(event){
    // Stop submit from performing default actions.
    event.preventDefault();

    // Get field values.
    var name = $('#playlist-name').val();
    var description = $('#playlist-description').val();
    var csrfToken = $('meta[name=csrf-token]').attr('content');

    // Toggle the playlist create controls.
    view.TogglePlaylistCreateControls();

    // Send the data to the backend.
    backendHandler.CreatePlaylist(name, description, csrfToken, view.UpdateListOfPlaylistsAndShowResult);
  });

  $('#start-playlist-creation').click(function(){
    view.HidePlaylistResult();
    view.TogglePlaylistCreateControls();
  });

  $('#cancel-playlist-creation').click(function(){
    view.TogglePlaylistCreateControls();
  });

  /* Search Button: Makes AJAX call to make search request */
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

    backendHandler.AddSongToPlaylist(playlist, track, csrfToken, view.UpdateAddSongSuccess);
  });
});