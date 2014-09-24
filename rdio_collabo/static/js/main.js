$(document).ready(function() {

  /* New playlist button: Makes AJAX call to request new empty playlist.*/
  $("#create-playlist").submit(function(){
    var name = $("#playlist-name").val();
    app.createPlaylist(name);
  })

  $("#nearby").text("Searching for nearby playlists...");
  app.nearby();

  /* Search Button: Makes AJAX call to make search request */
  $("#search").click(function(){
    $("#results").text("Loading...");
    var query = $("#query").val();
    app.search(query);
  })

});

/* App deals with logic for making AJAX calls.
View deals with displaying the page.
These objects are tightly coupled. :| */
app = {
  playlist: {},

  createPlaylist: function(name){
    $("#create-playlist").attr('action', '/playlists/new/' + name);
  },

  nearby: function(){
    $.post("/playlists/nearby", function(data, textStatus){
      console.log(textStatus);
      if(data == 0)
        view.printNoNearby();
      else{
        view.printNearby(data);
      }
    });
  },

  search: function(query){
    var self = this;
    $.post("/search/" + query, function(data, textStatus){
      var data = $.parseJSON(data);
      view.printResults(data);
      self.handleAdd();
    })
  },

  handleAdd: function(){
    var self = this;
    $(".add").click(function(){
      $.post("/add/" + this.id, function(data, textStatus){
        self.playlist = $.parseJSON(data);
        view.printPlaylist();
      });
    })
  }
};

view = {
  printPlaylist: function(){
    $("#results").html("Song added to playlist.");
    $("#results").after("<ul id='playlist'>");
    $.each(app.playlist, function(id, track) {
      $("#playlist").append("<li><ul id='playlist-" + id       + "'>");
      $("#playlist-" + id).append("Song: "        + track['name']  + "<br>");
      $("#playlist-" + id).append("Artist: "          + track['artist']    + "<br>");
      $("#playlist-" + id).append("Album: "          + track['album']    + "<br>");
    })
  },

  printResults: function(data){
    $("#results").html("<ul id='results-list'>");

    $.each(data, function(i, track) {
      var artist  = track["artist"];
      var name    = track["name"];
      var album   = track["album"];
      var art     = track["icon"];
      var id      = track["key"];

      $("#results-list").append("<li><ul id='result-"       + i       + "'>");
      $("#result-"  + i).append("<button class='add' id='"  + id      + "'>+</button><br>");
      $("#result-"  + i).append("Artist: "                  + artist  + "<br>");
      $("#result-"  + i).append("Name: "                    + name    + "<br>");
      $("#result-"  + i).append("Album: "                   + album   + "<br>");
      $("#result-"  + i).append("Rdio identifier: "         + id      + "<br>");
      $("#result-"  + i).append("<img src='"                + art     + "'><br>");
    });    
  },

  printNoNearby: function(){
    $("#nearby").text("No nearby playlists found. :(");
  },

  printNearby: function(data){
    $("#nearby").text("");
    for (var i = 0; i < data["playlists"].length; i++) {
      $("#nearby").append(data["playlists"][i].name + "<br>");
    };
  }
};