$(document).ready(function () {

    $('#login-form').submit(function (e) {
        e.preventDefault();
        var username = $('#username').val();
        var password = $('#userpassword').val();
        var remember = $('#customControlInline').val();
        console.log(password);
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        // set csrf header
        $.ajaxSetup({
            beforeSend: function (e, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    e.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $.ajax({
            url: "login/",
            method: "POST",
            data: { username: username, password: password, rememberMe: remember },
            dataType: 'json',
            success: function (response) {
                $('.alert').hide();
                console.log(response);
                var res = response;
                if (res.hasOwnProperty('success')) {

                    $('.sign-in').append('<div class="alert alert-success">Welcome</div>');
                    setTimeout(function () { $('.sign-in .alert').remove(); }, 1500);
                    window.location.href = '../home';

                } else if (res.hasOwnProperty('error')) {
                    $('.sign-in').append('<div class="alert alert-danger">' + res.error + '</div>');
                    setTimeout(function () { $('.sign-in .alert').remove(); }, 1500);
                }

            }
        });
    });
});