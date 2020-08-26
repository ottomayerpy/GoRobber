$(function() {
    function hovIn(obj) {
        levels = obj.attr('level');
        $('.desc-active').css('display', 'none');
        $('.levels_desc[level=' + levels + ']').css('display', 'block');
    }

    function hovOut(obj) {
        levels = obj.attr('level');
        $('.desc-active').css('display', 'block');
        $('.levels_desc[level=' + levels + ']').css('display', 'none');
    }

    $(".levels_progress-level").hover(function() {
        if (!$(this).hasClass('is-active'))
            hovIn($(this));
    }, function() {
        if (!$(this).hasClass('is-active'))
            hovOut($(this));
    });
});