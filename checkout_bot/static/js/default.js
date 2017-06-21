$(document).ready(function(){
  $('.messages').find('.alert').each(function(){
    var el = $(this);
    setTimeout(function(){
      el.fadeOut(500, function(){
       el.remove();
      });
    }, 4000);
  });

  $('.goto_page_numb').on('click', function(e){
    e.preventDefault();
    var url = $(this).attr('href') + '?page=' + $('#page_numb').val();
    window.location.href = url;
  });
});