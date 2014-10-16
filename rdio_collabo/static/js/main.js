$(document).ready(function() {

  
  $("#search-playlists").submit(function(event){
    event.preventDefault();

    var playlistQuery = $("search-playlists-query").val();
    var csrfToken = $('meta[name=csrf-token]').attr('content');

    backendHandler.SearchPlaylists(query, csrfToken, view.ShowSearchResults);
  });

  $('#create-playlist').submit(function(event){
    event.preventDefault();

    // Get field values
    var name = $('#playlist-name').val();
    var description = $('#playlist-description').val();
    var csrfToken = $('meta[name=csrf-token').attr('content');
    
    // Clear field values
    view.TogglePlaylistCreateControls();

    backendHandler.CreatePlaylist(name, description, csrfToken, view.UpdateListOfPlaylists);
  });

  /* Search Button: Makes AJAX call to make search request */
  $('#search').click(function(){
    $('#results').text('Loading...');
    var query = $('#query').val();
    var csrfToken = $('meta[name=csrf-token]').attr('content');
    backendHandler.SearchAlbumsArtistsTracks(query, csrfToken, view.PrintSearchResults);
  });

  $('#start-playlist-creation').click(function(){
    view.TogglePlaylistCreateControls();
  });

  $('#cancel-playlist-creation').click(function(){
    view.TogglePlaylistCreateControls();
  });

});

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

  SearchAlbumsArtistsTracks: function(query, csrfToken, viewFunction){
    $.ajax({url: "/search/" + query, 
      type: 'POST',
      dataType:'json',
      beforeSend:function(xhr){
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
      },
      success: function(data){
        if('ok' === data['status'])
        {
          // format data for view function.
          var result = data['result']['results'];
          viewFunction(result);
        }
      }
    });
  },

  SearchPlaylists: function(query, csrfToken, viewFunction){
    $.post('/search/playlists', 
      {
        'query': query, 
        'csrf_token': csrfToken
      }, 
      function(data){
        if('ok' === data['status'])
        {
          // format data for view function
          console.log(data);
          //viewFunction();
        }
    });
  }
};

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
        'href', '/playlists/' + result['key'])));
  },

  PrintSearchResults: function(result){
    $("#results").html("<ul id='results-list'>");

    $.each(result, function(i, track) {
      var artist  = track["artist"];
      var name    = track["name"];
      var album   = track["album"];
      var art     = track["icon"];
      var id      = track["key"];

      $("#results-list").append("<li><ul id='result-"       + i       + "'>");
      $("#result-"  + i).append("<button class='add btn btn-default' id='"  + id      + "'>+</button><br>");
      $("#result-"  + i).append("Artist: "                  + artist  + "<br>");
      $("#result-"  + i).append("Name: "                    + name    + "<br>");
      $("#result-"  + i).append("Album: "                   + album   + "<br>");
      $("#result-"  + i).append("Rdio identifier: "         + id      + "<br>");
      $("#result-"  + i).append("<img src='"                + art     + "'><br>");
    });    
  },


};