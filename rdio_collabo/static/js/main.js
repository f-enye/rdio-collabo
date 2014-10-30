$(document).ready(function() {
  // $("#search-playlists").submit(function(event){
  //   event.preventDefault();

  //   var playlistQuery = $("#search-playlists-query").val();
  //   var csrfToken = $('meta[name=csrf-token]').attr('content');

  //   backendHandler.SearchPlaylists(playlistQuery, csrfToken, view.ShowSearchResults);
  // });

  $("#join-playlist").submit(function(event){
      event.preventDefault();

      // Get field values.
      var playlistShareCode = $('#playlist-share-code').val();
      var url = 'http://' + window.location.host + "/playlists/" + playlistShareCode;

      console.log(window.location.host + "/playlists/" + playlistShareCode);
      location.replace(url);
  });

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
});