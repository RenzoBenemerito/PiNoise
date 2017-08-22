$(document).ready(function(){
    var categ = $('#category').text();
    $('#post').submit(function(){
        $('<input />').attr('type', 'hidden')
          .attr('name', "category")
          .attr('value', categ)
          .appendTo('#post');
      return true;
    });

    $('.delete').click(function(event){
        event.preventDefault();
        var choice = confirm();
        if(choice == true){
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
        }
        
    });

    $('.up,.down').click(function(){
        var pTitle = $(this).parent().next()
        var title = $(pTitle).first().find('h2').text();
        var author = $(pTitle).first().find('h4').text();
        var kind = $(this).attr('id')
        $.ajax({
            method: 'GET',
            url: 'vote',
            data: {
                'title':title,
                'kind':kind,
                'author':author,
            },
            datatype: 'json',
            success: function(){
                window.location.href = './';
            }
        });
    });


});