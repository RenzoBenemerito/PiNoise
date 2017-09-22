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
            var div = $(this).parents().eq(3);
            var title = $(this).parent().text();
            $.ajax({
                method: 'GET',
                url:'delete',
                data: {"title":title},
                datatype: 'json',
            })
            .done(function(){
                $(div).hide();
            });
        }
        
    });

    $('.up,.down').click(function(){
        var vote = $(this);
        var pTitle = $(this).parent().next()
        var title = $(pTitle).first().find('h2').text();
        var author = $(pTitle).first().find('h4').text();
        var kind = $(this).attr('id')
        var currentState = $(this).attr('style');

        if(kind == 'upvote'){
            var ratingObj = $(this).next();
            var rating = parseInt($(this).next().text());
        }
        else if(kind == 'downvote'){
            var ratingObj = $(this).prev();
            var rating = parseInt($(this).prev().text());
        }

        $.ajax({
            method: 'GET',
            url: 'vote',
            data: {
                'title':title,
                'kind':kind,
                'author':author,
            },
            datatype: 'json',
            success: function(event){
                if(kind == 'upvote'){
                    $('vote:hover').css('color','blue');
                    if(currentState == undefined || currentState == 'color: white;'){
                        $(vote).css('color','blue');
                        rating += 1;
                    }
                    else{
                        $(vote).css('color','white');
                        rating -= 1;
                    }
                    $(ratingObj).text(rating);
                }
                else if(kind == 'downvote'){
                    if(currentState == undefined || currentState == 'color: white;'){
                        $(vote).css('color','red');
                        rating -= 1;
                    }
                    else{
                        $(vote).css('color','white');
                        rating += 1;
                    }
                    $(ratingObj).text(rating);
                }
            }
        });
    });

    $('.update').submit(function(){
        var category = $('#category').text();
        $('<input />').attr('type', 'hidden')
          .attr('name', "category")
          .attr('value', category)
          .appendTo('.update');
      return true;
    });

    $('#updatePost').click(function(){
        $('#updatePost').css('display','none');
        $('.updatePane').removeAttr('style');
        $('.updatePane').css('display','block');
    });

    $(document).delegate('.replyForm','submit',function(evt){
        evt.preventDefault();
        var thisElement = $(this);
        var parent = $(this).parent().parent();
        var comment = parent.first().children('p').text();
        var author = parent.first().children('h4').text();
        var reply = $(this).find('#reply').val();
        var parent1 = $(this).parent().prev().prev();
        $.ajax({
            method: 'GET',
            url: './reply',
            data: {'comment':comment, 'author':author, 'reply':reply},
            success: function(obj){
                $(parent1).append(obj);
                $(thisElement.parent()).append(thisElement);
            }
        });
    });

    $('#commentForm').submit(function(event){
        event.preventDefault();
        var comment = $('.tarea').val();
        $.ajax({
            method: 'GET',
            url: './comment',
            data: {'comment': comment},
            success: function(obj){
                $('.commentPane').append(obj);
            }
        });
    });

    $(document).delegate('.deleteC', 'click', function(event){
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
                $(parent).hide();
            });
        }
        
    });

    $(document).delegate('.uComment', 'submit', function(evt){
        evt.preventDefault();
        var choice = confirm('Are you sure you want to edit your comment?');
        var uComment = $(this).find('.updateTar').val();
        if(choice == true){
            var parent = $(this).parents().eq(1);
            var comment = $(parent).children('p').text();
            var author = $(parent).children('h4').text();
            var changeThis = $(parent).children('p');
            var hideThis = $(this).parent();
            var button = $(this).parent().prev();
            $.ajax({
                method: 'GET',
                url:'./editComment',
                data: {"comment":comment,'uComment':uComment,'author':author},
                datatype: 'json',
                success: function(){
                    $(hideThis).hide();
                    $(changeThis).text(uComment);
                    $(button).text('Edit');
                    $(button).removeClass('btn-danger')
                    $(button).addClass('btn-success')
                }
            })
        }
        
    });

    $(document).delegate('.uReply', 'submit', function(evt){
        evt.preventDefault();
        var choice = confirm('Are you sure you want to edit your reply?');
        
        if(choice == true){
            var parent = $(this).parents().eq(1);
            var uReply = $(this).children('.updateTar').val();
            var comment = $(parent).children('p').text();
            var author = $(parent).children('h4').text();
            var authorC = $(this).parents().eq(3).children('h4').text();
            var commentC = $(this).parents().eq(3).children('p').text();
            var changeThis = $(parent).children('p');
            var hideThis = $(this).parent();
            var button = $(this).parent().prev();
            $.ajax({
                method: 'GET',
                url:'./editReply',
                data: {"comment":comment,'uReply':uReply,'author':author,'authorC':authorC,'commentC':commentC},
                datatype: 'json',
                success: function(){
                    $(hideThis).hide();
                    $(changeThis).text(uReply);
                    $(button).text('Edit');
                    $(button).removeClass('btn-danger')
                    $(button).addClass('btn-success')
                }
            })
        }
        
    });
    $(document).delegate('.deleteR','click',function(event){
        event.preventDefault();
        var choice = confirm('Are you sure you want to delete your comment?');
        if(choice == true){
            var parent = $(this).parent();
            var comment = $(parent).children('p').eq(0).text();
            var author = $(this).parent().children('h4').eq(0).text();
            var authorC = $(this).parents().eq(2).children('h4').text();
            var commentC = $(this).parents().eq(2).children('p').text();
            $.ajax({
                method: 'GET',
                url:'deleteReply',
                data: {"comment":comment,'author':author,'authorC':authorC,'commentC':commentC},
                datatype: 'json',
            })
            .done(function(){
                $(parent).hide();
            });
        }
        
    });

    $(document).delegate('.updateC','click',function(){
        var state = $(this).text();
        if(state == "Edit"){
            $(this).next().show();
            $(this).text('Cancel');
            $(this).removeClass('btn-success')
            $(this).addClass('btn-danger')
        }
        else if(state == "Cancel"){
            $(this).next().hide();
            $(this).text('Edit');
            $(this).removeClass('btn-danger')
            $(this).addClass('btn-success')
        }
        
    });

    $(".toggle-icon").click(function(){
        $(".nav").toggleClass('statusNav');

    });
    // $('#report').submit(function(){
    //     var post = $(this).parents().eq(3).prev().find('h2').eq(0).text();
    //     var author = $(this).parents().eq(3).prev().find('span#auth').eq(0).text();
    //     var category = $(this).parents().eq(3).prev().find('span#category').eq(0).text();
    // });

});