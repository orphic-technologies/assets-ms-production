$(document).ready(function () {
    $('input[type="checkbox"]').click(function () {
        var arrayselected = $.map($('input[name="selectedavailable"]:checked'), function (c) { return c.value; });
        var arraynotselected = $.map($('input[name="selectedavailable"]:not(:checked)'), function (c) { return c.value; });
        valueincookie = $.cookie('valueincookie')

        // if cookie isnt set, it cannot parse as json so we must check this condition
        if (typeof valueincookie != 'undefined') {
            valueincookie = JSON.parse($.cookie('valueincookie'))
            console.log('defined', valueincookie)
        } else {
            valueincookie = []
        }
        // ---------------------------------------------------------------------------

        console.log("checked", arrayselected)
        console.log("unchecked", arraynotselected)

        //-- for adding the value which is not present in cookie -------------------------------
        valueincookie.push(...arrayselected);
        valueincookie = valueincookie.filter((val, index, self) => self.indexOf(val) === index);
        //--------------------------------------------------------------------------------------

        // ----for removing the value which is not checked
        valueincookie = valueincookie.filter((el) => !arraynotselected.includes(el));

        console.log(valueincookie)
        $.cookie('valueincookie', JSON.stringify(valueincookie), { path: '/' });

        // ----- to show in top panel,----------- 
        var cookievalues = ($.cookie('valueincookie'))
        cookievalues = cookievalues.replace(/'/g, '"');
        cookievalues = JSON.parse(cookievalues);
        var cookieLength = cookievalues.length;
        //-------------------------------------
        if (cookieLength <= 0) {
            $('.noti-dot').hide();
        }
        else {
            document.getElementById("spanadd").innerHTML += `<span class="noti-dot"></span>`;
        }
        document.getElementById("toadd").innerHTML = "";
        //- -----------
        for (var i = 0; i < cookieLength; i++) {

            document.getElementById("toadd").innerHTML += `<div data-simplebar style="max-height: 230px;">
            <div class="text-reset notification-item">
                <div class="d-flex">
                    <div class="flex-shrink-0 me-3 p-1 remove removeselected" id="`+ cookievalues[i] + `">
                    
                        <div class="avatar-xs">
                            <span class="avatar-title bg-danger rounded-circle">
                                <i class="mdi mdi-minus-thick"></i>
                            </span>
                        </div>
                    </div>
                    <div class="flex-grow-1">
                        
                        <div class="font-size-12 text-muted">
                        <h6 class="mb-1">`+ cookievalues[i] + `</h6>
                            <p class="mb-1">`+ cookievalues[i] + `</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>`;
        }
    })

    $('#available-form').submit(function (e) {
        e.preventDefault();
        var checkasset = {};

        // values to be sent ------------------
        var cookievalue = ($.cookie('valueincookie'))
        cookievalue = cookievalue.replace(/'/g, '"');
        cookievalue = JSON.parse(cookievalue);
        console.log(cookievalue)
        var cookieLength = cookievalue.length;
        cookieLength

        for (var i = 0; i < cookieLength; i++) {
            checkasset[cookievalue[i]] = 1;
        }
        // -------------------------------------
        if (cookieLength <= 0) {

            alert("you haven't selected any assets");
        }
        else {
            const convertedcheckasset = JSON.stringify(checkasset)
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
                url: "../../assignassettemplate/",
                method: "POST",
                data: { dictval: convertedcheckasset },
                dataType: 'json',
                success: function (response) {
                    $('.alert').hide();
                    console.log(response);
                    window.location.href = '../../assignasset/' + JSON.stringify(response);
                }
            });
        }

    });
});