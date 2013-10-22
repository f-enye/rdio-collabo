$(document).ready(function() {

  /* Search Button: Makes AJAX call to make search request */
  $("#search").click(function(){
    $("#results").text("Loading...");
    var query = $("#query").val();
    app.search(query);
  })

});

/* Object to house all collaborative playlist functions */
app = {
  search: function(query){
    var self = this;
    $.post("/search/" + query, function(data, textStatus){
      var data = $.parseJSON(data);
      self.printResults(data);
    })
  },

  printResults: function(data){
    $("#results").text("");
    $.each(data, function(i, track) {
      $("#results").append(i+": ");
      var artist = track["artist"];
      var name = track["name"];
      var album = track["album"];
      var art = track["icon"];
      var id = track["key"];
      $("#results").append("Artist: "+artist+"<br>");
      $("#results").append("Name: "+name+"<br>");
      $("#results").append("Album: "+album+"<br>");
      $("#results").append("rdio identifier: "+id+"<br>");
      $("#results").append("<img src='"+art+"'><br>");
    })
  }
};