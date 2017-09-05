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
        var choice = confirm('Are you sure you want to delete your idea?');
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

    $('.reply').click(function(){
        $('.replyForm').removeAttr('style');
        $('.replyForm').css('display','block');
    });

    $('.replyForm').submit(function(){
        var parent = $(this).parent().parent();
        var comment = parent.first().children('p').text();
        var author = parent.first().children('h4').text();
        $('<input />').attr('type', 'hidden')
        .attr('name', "comment")
        .attr('value', comment)
        .appendTo('.replyForm');
        $('<input />').attr('type', 'hidden')
        .attr('name', "author")
        .attr('value', author)
        .appendTo('.replyForm');
    });

    $('.deleteC').click(function(event){
        event.preventDefault();
        var choice = confirm('Are you sure you want to delete your comment?');

        if(choice == true){
            var parent = $(this).parent();
            var comment = $(parent).children('p').text();
            var author = $(this).parent().children('h4').text();
            $.ajax({
                method: 'GET',
                url:'deleteComment',
                data: {"comment":comment,'author':author},
                datatype: 'json',
            })
            .done(function(){
                window.location.href = './post_page';
            });
        }
        
    });

    $('.deleteR').click(function(event){
        event.preventDefault();
        var choice = confirm('Are you sure you want to delete your comment?');

        if(choice == true){
            var parent = $(this).parent();
            var comment = $(parent).children('p').eq(0).text();
            var author = $(this).parent().children('h4').eq(0).text();
            $.ajax({
                method: 'GET',
                url:'deleteReply',
                data: {"comment":comment,'author':author},
                datatype: 'json',
            })
            .done(function(){
                window.location.href = './post_page';
            });
        }
        
    });

    // $('#report').submit(function(){
    //     var post = $(this).parents().eq(3).prev().find('h2').eq(0).text();
    //     var author = $(this).parents().eq(3).prev().find('span#auth').eq(0).text();
    //     var category = $(this).parents().eq(3).prev().find('span#category').eq(0).text();
    // });

});