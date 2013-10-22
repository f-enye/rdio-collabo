$(document).ready(function() {

  /* Search Button: Makes AJAX call to make search request */
  $("#search").click(function(){
    $("#results").text("Loading...");
    var query = $("#query").val(); // TODO: Sanitize and URL encode input
    collabo.search(query);
  })

});

/* Object to house all collaborative playlist functions */
collabo = {
  search: function(query){
    var self = this;
    $.post("/search/" + query, function(data, textStatus){
      var data = $.parseJSON( data );
      self.results(data);
    })
  },

  results: function(data){
    $("#results").text("");
    $.each(data, function(i, track) {
      $("#results").append(i+": ");
      var artist = track["artist"];
      var name = track["name"];
      var album = track["album"];
      $("#results").append("Artist: "+artist+"<br>Name: "+name+"<br>Album: "+album+"<br><br>");
    })
  }
};