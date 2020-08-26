$(function() { // Start JS
    window.socket;
    window.red = '#ED9AA2';
    window.green = '#93D3A2';
    window.blue = '#8BD0DB';
    window.yellow = '#FFE083';
    window.white = '#FFFFFF';
    window.newToast = newToast;
    window.base_socket_onmessage = base_socket_onmessage;
    window.newBalance = newBalance;

    if (window.location.protocol == 'https:') {
        socket = new WebSocket('wss://' + window.location.host + window.location.pathname);
    } else {
        socket = new WebSocket('ws://' + window.location.host + window.location.pathname);
    }

    socket.onclose = function() { // Сигнал закрытия сокета
        newToast('Сервер', 'Разорвано соединение с сервером, перезагрузите страницу', red);
    }

    socket.onmessage = function(event) {
        var message = JSON.parse(event.data);
        base_socket_onmessage(message.head, message.data);
    }

    function base_socket_onmessage(head, data) {
        if (head == 'send_message') {
            if (data == 'success') {
                $('#result').fadeIn(1000);
                $('#result').fadeOut(500);
                setTimeout(() => {
                    $('#name').val('');
                    $('#email').val('');
                    $('#message').val('');
                }, 1000);
            }
        } else if (head == 'Pay' || head == 'PayOut') {
            if (data.status == 'success') {
                newBalance(data.balance);
                if (head == 'Pay')
                    newToast('Финансы', 'Баланс пополнен', green);
                else
                    newToast('Финансы', 'Деньги выведены', green);
            } else {
                newToast('Финансы', 'Ошибка операции', red);
            }
        } else if (head == 'Error') {
            if (data.description == 'create_game_negative-balance') {
                newToast('Ошибка', 'Недостаточно средств', yellow);
                $('.game_start_button').text('Начать игру за ' + data.case_cost + '₽');
                active = false;
            } else if (data.description == 'NoneCommand') {
                newToast('Ошибка', 'Не известная команда', red);
            } else if (data.description == 'create_game_low-level') {
                newToast('Ошибка', 'Ваш уровень не соответствует уровню кейса', yellow);
            } else {
                newToast('Ошибка', data.description, red);
            }
        } else if (head == 'update_counter_online_users') {
            $('#online-counter').text(data);
        } else if (head == 'StatGames') {
            $('#case-counter').text(data);
        } else if (head == 'new_coin_in_live_tape') {
            newBlock = '<a href="/profile/id' + data.id +
            '/"><div class="coin-block-min__coin-glow"></div><img src="/static/img/prizes/' +
            data.cost + '.png" class="coin-block-min__coin-img image first"><img src="' +
            data.avatar + '" class="coin-block-min__coin-img image second"></a>';

            $('.coin-block-min__new').append(newBlock);
            $('.coin-block-min__new').addClass('coin-block-min_none');
            $('.coin-block-min__new').addClass('ImgField');
            $('.coin-block-min__new').removeClass('coin-block-min__new');
            if ($('.coin-block-min_none').length == 12) {
                $('.coin-block-min_none:last').remove();
            }
            var new_min = $('.coin-block-min__new_min')
            new_min.css({ width: 90 });
            new_min.removeClass('coin-block-min__new_min')
            new_min.addClass('coin-block-min__new')
            $('.live_tape_line-coins').prepend('<div class="coin-block-min coin-block-min__new_min"></div>');
        } else if (head == 'levels') {
            newToast('Уровни', 'Вы повышены на ' + data + ' уровень!', green);
        }
    }

    $('button[name=buttonPay]').on('click', function() {
        data = {
            'command': 'Pay',
            'userid': $('body').data('userId'),
            'value': $('input[name=inputPay]').val()
        }

        socket.send(JSON.stringify(data));
    });

    $('button[name=buttonPayOut]').on('click', function() {
        data = {
            'command': 'PayOut',
            'userid': $('body').data('userId'),
            'value': $('input[name=inputPayOut]').val()
        }

        socket.send(JSON.stringify(data));
    });

    // При открытии модальных окон скрыть кнопку меню
    $('#RegModal, #PreRegModal, #ExitModal, #Pay, #PayOut').on('show.bs.modal', function() {
        if ($('body').innerWidth() <= 974)
            $(".btn-hamburger").css({
                display: 'none'
            });
    });

    // При закрытии модальных окон показать кнопку меню
    $('#RegModal, #PreRegModal, #ExitModal, #Pay, #PayOut').on('hide.bs.modal', function() {
        if ($('body').innerWidth() <= 974)
            $(".btn-hamburger").css({
                display: ''
            });
    });

    window.onbeforeunload = function() { // Сделать затухание при преходах по ссылками на сайте
        $('.windows8').removeClass('preload-done');
        $('.windows8').css({ display: '' });
        $('#page-preload').removeClass('preload-done');
    }

    $(window).resize(function() { // Изменение логотипа в соответствии размерам окна
        if ($('body').innerWidth() <= 974)
            $('.logotype').find('p').html('<span>G</span>R');
        else
            $('.logotype').find('p').html('<span>Go</span>Robber');
    });

    $(document).ready(function() {
        $('#page-preload').addClass('preload-done');
        $('.windows8').addClass('preload-done');
        setTimeout(function() {
            $('.windows8').css({ display: 'none' });
        }, 1000);

        var slideout = new Slideout({
            'panel': document.getElementById('panel'),
            'menu': document.getElementById('menu'),
            'side': 'right'
        });

        document.querySelector('.js-slideout-toggle').addEventListener('click', function() {
            slideout.toggle();
        });

        document.querySelector('.menu').addEventListener('click', function(eve) {
            if (eve.target.nodeName === 'A') {
                slideout.close();
            }
        });
    });

    $(window).resize(function() {
        $('.windows8').css({
            position: 'absolute',
            left: ($(window).width() - $('.windows8').outerWidth()) / 2,
            top: ($(window).height() - $('.windows8').outerHeight()) / 2
        });
    });
    $(window).resize();

    function newBalance(balance) { // Анимированное изменение баланса
        var profile_balance = $('.home-profile_balance').find('span');
        $({ numberValue: profile_balance.text() }).animate({ numberValue: balance }, {
            duration: 2000,
            easing: "linear",
            step: function(val) {
                profile_balance.text(Math.ceil(val));
            }
        });
    }

    function newToast(title, text, color) {
        if ($('.toast').length >= 5) {
            $('.toast:last').remove();
        }
        element = '<div style="margin-right:10px;margin-top:10px;background:' + color +
        '" data-autohide="false" class="toast" role="alert" aria-live="assertive"' +
        'aria-atomic="true"><div class="toast-header"><strong class="mr-auto">' +
        title + '</strong><button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">' +
        '<span aria-hidden="true">&times;</span></button></div><div class="toast-body">' + text + '</div></div>';

        $('#toast-container').prepend(element);
        $('.toast.hide').remove();
        toast = $('.toast');
        toast.toast('show');

        setTimeout(() => {
            $(toast).remove();
        }, 5000);
    }
});