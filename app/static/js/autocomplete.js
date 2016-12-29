function autocomplete(elem, url) {
  $(elem).autocomplete({
    source: function(request, response){
      $.getJSON(url,{
        q: request.term,
      }, function(data) {
        response(data.matching_results);
      });
    },
    minLength: 1,
    select: function(event, ui){
    }
  });
}
