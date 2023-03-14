$(".dropdown dt a").on('click', function(){
    $(".dropdown dd ul").slideToggle('fast')
});

$('.multiselect input[type="checkbox"]').on('click', function(){
    var title = $(this).closest('.multiselect').find('input[type="checkbox"]').val(),
        title = $(this).val() + " - ";

    if($(this).is(':checked')){
        var html = '<span title="'+title+'">' + title + '</span>';
        $('.list').append(html);
        $('.hide').hide()
    }
    else{
        $('span[title="'+title+'"]').remove();
        var ret = $('.hide');
        $('.dropdown dt a').append(ret);
    }
});
