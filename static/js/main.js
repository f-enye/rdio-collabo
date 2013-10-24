$(document).ready(function() {

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
  playlist: [],

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
        console.log(textStatus);
        console.log(data);
        console.log("Id:" + this.id);
        self.playlist = data;
        view.printPlaylist();
      });
    })
  }
};

view = {
  printPlaylist: function(){
    console.log(app.playlist);
    $("#results").html("Song added to playlist.");
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
  }
};