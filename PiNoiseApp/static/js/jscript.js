$(document).ready(function(){
    $(window).scroll(function(){
        console.log($(window).scrollTop());
        if($(this).scrollTop()>25){
            $('nav').addClass('nav-scroll');
            $('.nav>li>a').addClass('nav-scroll-a');
            $('.nav>li>a:hover .nav>li>a:active').addClass('nav-scroll-a:hover');
            $('.icon-bar').addClass('bgBlack');
            $('body').css('padding-top:5.5%;');
        }
        else{
            $('nav').removeClass('nav-scroll');
            $('.nav>li>a:hover .nav>li>a:active').removeClass('nav-scroll-a:hover');
            $('.nav>li>a').removeClass('nav-scroll-a');
            $('.icon-bar').removeClass('bgBlack');
            $('body').css('padding-top:0;');
        }
    $('body').scrollspy({ target: '.navbar' });
    });
});
$('a[href*="#"]')
  // Remove links that don't actually link to anything
  .not('[href="#"]')
  .not('[href="#0"]')
  .click(function(event) {
    // On-page links
    if (
      location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') 
      && 
      location.hostname == this.hostname
    ) {
      // Figure out element to scroll to
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      // Does a scroll target exist?
      if (target.length) {
        // Only prevent default if animation is actually gonna happen
        event.preventDefault();
        $('html, body').animate({
          scrollTop: target.offset().top-50
        }, 500, function() {
          // Callback after animation
          // Must change focus!
          var $target = $(target);
          $target.focus();
          if ($target.is(":focus")) { // Checking if the target was focused
            return false;
          } else {
            $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
            $target.focus(); // Set focus again
          };
        });
      }
    }
    
  });
  $('#login').click(function(){
      $('.log-in-pane').css("width","25%");
  });
  $('.close1').click(function(){
    $('.log-in-pane').css("width","0");
  });
