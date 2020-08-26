$(function() {
    var button, // Текущая нажатая ячейка на игровом поле
        click = false, // Можно нажать на ячейку или нет
        active = false,
        end_game,
        game_start_button_text,
        quantity_cells_available = 12;

    socket.onopen = function() {
        data = {
            'command': 'get_game',
            'case': $('.js-case-name').text(),
            'userid': $('body').data('userId')
        }
        socket.send(JSON.stringify(data));
    }

    socket.onmessage = function(event) {
        var message = JSON.parse(event.data);
        base_socket_onmessage(message.head, message.data);
        case_socket_onmessage(message.head, message.data);
    }

    function case_socket_onmessage(head, data) {
        if (head == 'get_game') {
            $('.block-start').css("display", "none");
            for (var key in data.open_cells) {
                var block = $('.game-cell[data-cell="' + key + '"]');
                block.find('img').attr('src', '/static/img/prizes/' + data.open_cells[key] + '.png');
                block.data('done', true);
                block.find('img').data('done', true);
                block.find('img').css("cursor", "auto");
            }

            if (data.quantity_cells_available == 0) {
                $('.block-continue-button').css("display", "none");
                $('.block-pause').fadeIn(); // Показываем кнопки продолжить и начать заного
                click = false;
            } else {
                click = true;
                quantity_cells_available = data.quantity_cells_available;
            }

            if (data.sum_win != 0) {
                $('.pick_up_money_sum').text(data.sum_win);
            } else {
                $('.js-game-pick-up-money-button').css("display", "none");
            }
        } else if (head == 'play_game') {
            button.find('img')[0].src = '/static/img/prizes/' + data.win + '.png'; // Заполняем сорс блока
            button.find('img').removeClass('spin_image');
            if (data.win == 0) {
                $('.block-restart').fadeIn(); // Показываем кнопку рестарта игры
                click = false; // Ставим метку завершения игры
                quantity_cells_available = 12;
                var end_data = {
                    'command': 'end_game',
                    'win': false,
                    'case': $('.js-case-name').text(),
                    'userid': $('body').data('userId')
                }
                socket.send(JSON.stringify(end_data))
            } else {
                quantity_cells_available--;
                if (quantity_cells_available == 0)
                    $('.block-continue-button').css("display", "none"); // Скрываем кнопку продолжить так как пользователь выиграл
                $('.pick_up_money_sum').text(data.sum_win);
                $('.block-pause').fadeIn(); // Показываем кнопки продолжить и начать заного
                click = true;
            }
            if (!$(".js-game-pick-up-money-button").is(":visible"))
                $('.js-game-pick-up-money-button').css("display", "block");
        } else if (head == 'end_game') {
            end_game = data.unopened_cells
            if (data.win) {
                newBalance(data.balance);
                openCard(data.unopened_cells); // Открываем все ячейки
                $('.block-pause').fadeOut(); // Скрываем кнопки продолжить и забрать выигрыш
                quantity_cells_available = 12;
                setTimeout(() => {
                    $('.game-cell').find('img').attr('src', '/media/cells/' + $('body').data('cardId') + '.png'); // Вернуть дефолтную картинку для блоков
                    $('.block-start').fadeIn(); // Показываем кнопку старта игры
                    $('.pick_up_money_sum').text(0); // Задаем текст для кнопки "Забрать выигрыш"
                }, 2000);
                setTimeout(() => {
                    active = false;
                }, 1000);
            }
        } else if (head == 'create_game') {
            var balance = data.balance;
            newBalance(balance);
            $('.game-cell').find('img').attr('src', '/media/cells/' + $('body').data('cardId') + '.png'); // Вернуть дефолтную картинку для блоков
            quantity_cells_available = data.quantity_cells_available;
            $('.game-cell').data('done', false); // Переводим все блоки в режим "Не использованно"
            $('.game-cell').find('img').css("cursor", "pointer"); // Переводим курсор для всех блоков в режим поинт
            $('.block-continue-button').css("display", "block"); // Возвращаем отображение кнопки продолжить
            $('.block-start').fadeOut(); // Скрываем кнопку старта игры
            click = true; // Задаем что кликать можно
            setTimeout(() => {
                active = false;
                $('.block-start-button').text(game_start_button_text);
            }, 1000);
        }
    }

    $('.game-cell').on('click', function() { // Событие нажатия ячейки на игровом поле
        if ($(this).data('done') || click == false) // Если нажатая ячейка использована или клик не разрешен, то пропускаем нажатие
            return;
        click = false;
        button = $(this);
        button.data('done', true); // Переводим нажатый блок в режим "Использованно"
        button.find('img').css("cursor", "auto"); // Переводим курсор в дефолтный режим для ипользованного блока
        button.find('img').addClass('spin_image');

        data = {
            'command': 'play_game',
            'case': $('.js-case-name').text(),
            'cell': $(this).attr('data-cell'),
            'userid': $('body').data('userId')
        }

        socket.send(JSON.stringify(data))
    });

    $('.block-start-button').on('click', function() { // Событие нажатия кнопки старта игры
        if (active)
            return;
        active = true;

        game_start_button_text = $(this).text();
        $(this).text('Обработка...');

        data = {
            'command': 'create_game',
            'case': $('.js-case-name').text(),
            'userid': $('body').data('userId')
        }

        socket.send(JSON.stringify(data))
    });

    $('.js-game-pick-up-money-button').on('click', function() { // Событие нажатия кнопки забрать выигрыш
        if (active)
            return;

        active = true;

        data = {
            'command': 'end_game',
            'win': true,
            'case': $('.js-case-name').text(),
            'userid': $('body').data('userId')
        }

        socket.send(JSON.stringify(data))
    });

    $('.block-continue-button').on('click', function() { // Событие нажатия кнопки продолжить игру
        if (active)
            return;

        active = true;

        $('.block-pause').fadeOut(); // Скрываем кнопки продолжить и забрать выигрыш

        setTimeout(() => {
            active = false;
        }, 1000);
    });

    $('.block-restart-button').on('click', function() { // Событие нажатия кнопки начать заново
        if (active)
            return;

        active = true;
        $('.block-restart-button').text('Обработка...');
        $('.block-restart').fadeOut(); // Скрываем кнопку рестарта игры
        openCard(end_game); // Открываем все ячейки
        setTimeout(() => {
            $('.game-cell').find('img').attr('src', '/media/cells/' + $('body').data('cardId') + '.png'); // Вернуть дефолтную картинку для блоков
            $('.block-continue-button').css("display", "block");
            $('.block-start').fadeIn(); // Показываем кнопку старта игры
            $('.pick_up_money_sum').text(0); // Задаем текст для кнопки "Забрать выигрыш"
        }, 2000);
        setTimeout(() => {
            active = false;
        }, 1000);
        setTimeout(() => {
            $('.block-restart-button').text('Начать заново');
        }, 1000);
    });

    function openCard(mass) { // Открывает все остальные блоки в случае проигрыша или если пользователь заберет выигрыш
        var case_item = 0;
        for (i = 1; i <= 12; i++) {
            var block = $('.game-cell[data-cell="' + i + '"]');
            if (block.data('done') !== true) { // Пропускаем блоки с атрибутом done (т.е. открытые)
                block.data('done', true);
                block.find('img').attr('src', '/static/img/prizes/' + mass[case_item] + '.png'); // Заполняем сорс блоков
                block.find('img').css("cursor", "auto");
                case_item++;
            }
        }
    }
});