$(document).ready(function(){
    var categ = $('#category').text();
    $('#post').submit(function(){
        $('<input />').attr('type', 'hidden')
          .attr('name', "category")
          .attr('value', categ)
          .appendTo('#post');
      return true;
    });

    $('#searchForm').submit(function(){
        $('<input />').attr('type', 'hidden')
          .attr('name', "category")
          .attr('value', categ)
          .appendTo('#searchForm');
      return true;
    });

    $('#sortForm').submit(function(){
        var val = $("input[type=submit][clicked=true]").val();
        $('<input />').attr('type', 'hidden')
          .attr('name', "category")
          .attr('value', categ)
          .appendTo('#sortForm');
         $('<input />').attr('type', 'hidden')
          .attr('name', "sortBy")
          .attr('value', val)
          .appendTo('#sortForm');
      return true;
    });

    $("form input[type=submit]").click(function() {
        $("input[type=submit]", $(this).parents("form")).removeAttr("clicked");
        $(this).attr("clicked", "true");
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

    $('#update').submit(function(){
        var category = $('#category').text();
        $('<input />').attr('type', 'hidden')
          .attr('name', "category")
          .attr('value', category)
          .appendTo('#update');
      return true;
    });

    $('#updatePost').click(function(){
        $('#updatePost').css('display','none');
        $('.updatePane').removeAttr('style');
        $('.updatePane').css('display','block');
    });

});