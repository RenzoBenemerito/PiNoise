$(document).ready(function(){
    var categ = $('#category').text();
    $('#post').submit(function(){
        $('<input />').attr('type', 'hidden')
          .attr('name', "category")
          .attr('value', categ)
          .appendTo('#post');
      return true;
    });
    $('#delete').click(function(event){
        event.preventDefault();
        var title = $(this).parent().text();
        $.ajax({
            method: 'GET',
            url:'delete',
            data: {"title":title},
            datatype: 'json',
        })
        .done(function(){
            window.location.href = './';
        });
    });

});