$(function() {
    // Отправка сообщений в техническую поддержку
    $('.js-send_message').on('click', function() { // Проверяет отмечен ли чекбокс согласия
        if ($("#check").prop("checked")) {
            data = {
                'command': 'send_message',
                'username': $('#name').val(),
                'email': $('#email').val(),
                'message': $('#message').val(),
                'userid': $('body').data('userId')
            }

            socket.send(JSON.stringify(data))
            newToast('Техническая поддержка', 'Сообщение отправлено. Ожидайте обратной связи.', green);
        } else {
            newToast('Техническая поддержка', 'Поставьте галочку на пункте "Я добровольно отправляю свои данные"', yellow);
        }
    });
});