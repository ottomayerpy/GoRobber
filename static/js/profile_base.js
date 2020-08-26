$(function() { // Start JS
    if (window.location.pathname == '/profile/finance/') { // Если открыта страница финансов то сделать кнопку финансов активной
        $('.js-button_finance').removeClass('ButtonReg')
        $('.js-button_finance').addClass('ButtonRegActive')
    } else if (window.location.pathname == '/profile/levels/') { // Если открыта страница уровней то сделать кнопку уровней активной
        $('.js-button_levels').removeClass('ButtonReg')
        $('.js-button_levels').addClass('ButtonRegActive')
    } else { // Если открыта страница профиля то сделать кнопку профиля активной
        $('.js-button_prof').removeClass('ButtonReg')
        $('.js-button_prof').addClass('ButtonRegActive')
    }
});