$(document).ready(function(){
  view = {
    TogglePlaylistCreateControls: function(){
      // Hide the start playlist creation button.
      $("#start-playlist-creation").toggle();

      // Reset the form.
      $('#create-playlist')[0].reset();
      
      // Hide the form.
      $('#create-playlist').toggle();
    },

    UpdateListOfPlaylists: function(result){
      $('#owner-playlists').append(
        $('<li></li>').append($('<a></a>').text(result['name']).attr(
          'href', '/playlists/' + result['id'])));
    },

    UpdateListOfPlaylistsAndShowResult: function(result){
      view.UpdateListOfPlaylists(result);
      view.ShowPlaylistResult(result);
    },

    HidePlaylistResult: function(){
      $("#playlist-result").hide();
    },

    ShowPlaylistResult: function(result){
      var playlistResult =  $("#playlist-result");
      playlistResult.show();
      playlistResult.children("p").remove();
      playlistResult.append($("<p></p>").text("Playlist Code: " + result['id']));
    },

    AddToTrackList: function(track){
      var songList = $('#song-nominate-list');

      songList.children('dl').remove();
      artistListItem = $('<dl></dl>');
      songList.append(artistListItem.append($('<dt>Artist:</dt>')).append($("<dd>" + track['artist'] + "</dd>").attr('id', 'artist')));
      songList.append(artistListItem.append($('<dt>Name:</dt>')).append($("<dd>" + track['name'] + "</dd>").attr('id', 'name')));
      songList.append(artistListItem.append($('<dt>Key:</dt>')).append($("<dd>" + track['key'] + "</dd>").attr('id', 'key')));
    },

    PrintSearchResults: function(result){
      $("#results").append($("<ul id='results-list'></ul>"));

      $.each(result, function(i, track) {
        var artist  = track['artist'];
        var name    = track['name'];
        var album   = track['album'];
        var art     = track['icon'];
        var id      = track['key'];

        var listItem = $('<dl></dl>').append("<button class=' add btn btn-default' type='button'>+</button><br>");
        listItem.append($('<dt>Artist:</dt>')).append("<dd class='artist'>" + artist + "</dd>");
        listItem.append($('<dt>Name:</dt>')).append("<dd class='name'>" + name + "</dd>");
        listItem.append($('<dt>Album</dt>')).append("<dd class='album'>" + album + "</dd>");
        listItem.append($('<dt>Key</dt>')).append("<dd class='key'>" + id + "</dd>");
        listItem.append("<img src='"+ art + "'><br>");
        $('#results-list').append(listItem);
      });  

      // Add click triggered function to the add buttons.
      $('.add').click(function(evt){
        var targetsParent = $(evt.target).parent();
        var track = {};

        track['artist'] = targetsParent.children('.artist').text();
        track['name'] = targetsParent.children('.name').text();
        track['key'] = targetsParent.children('.key').text();
        view.AddToTrackList(track);
      });
    },

    UpdateAddTrackSuccess: function(result){
      $('#voting-section').append('<li>Name: ' + result['result']['name'] + ", By: " + result['result']['artist'] + '</li>');
    },

    UpdateJoined: function(result){
      console.log(result);
    },
  };
});