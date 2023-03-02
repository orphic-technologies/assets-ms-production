$(document).ready(function () {

    $('#release-button').click(function (e) {
        e.preventDefault();
        var checkasset = {};
        var dateofr = $('#dateofr').val();
        console.log(dateofr)
        var table = document.getElementById('table-release');
        var countselect = 1;
        if (dateofr == "") {
            alert("you haven't given date of return");
        }
        else {
            for (var i = 1; i < table.rows.length; i++) {
                if (table.rows[i].cells.length) {
                    var asset_code = (table.rows[i].cells[0].querySelector("#assetcode").innerText);
                    var token = (table.rows[i].cells[0].querySelector("#token").innerText);
                    var condition = (table.rows[i].cells[2].querySelector("#releasecondition option:checked")).innerText;
                    var ischecked = (table.rows[i].cells[3].querySelector('.form-check #customCheck4:checked'));

                    stripped_token = token.split(' ').join('');
                    trim_condition = condition.trim();
                    console.log(stripped_token);
                    console.log(trim_condition)

                    if (ischecked != null) {
                        console.log(asset_code);
                        checkasset[asset_code] = trim_condition;
                        console.log(checkasset);
                    }
                    else {
                        countselect += 1;
                    }
                }
            }
            if (countselect == table.rows.length) {
                console.log("here")
                console.log(countselect)
                alert("you haven't selected any assets");
            }
            else {
                const convertedreleaseasset = JSON.stringify(checkasset)
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
                    url: "../../releaseassetone/",
                    method: "POST",
                    data: { dictval: convertedreleaseasset, token: stripped_token, dateofreturn: dateofr },
                    dataType: 'json',
                    success: function (response) {
                        $('.alert').hide();
                        console.log(response);
                        if (response.hasOwnProperty('success')) {
                            console.log(response.success)
                            $('.show-message').append('<div class="alert alert-success">' + response.success + '</div>');
                            setTimeout(function () { $('.show-message .alert').remove(); }, 5000);
                            window.location.href = '../../product/usedassets/';

                        } else if (response.hasOwnProperty('error')) {
                            $('.show-message').append('<div class="alert alert-danger">' + response.error + '</div>');
                            setTimeout(function () { $('.show-message .alert').remove(); }, 5000);
                        }
                    }
                });
            }

        }
    });
});