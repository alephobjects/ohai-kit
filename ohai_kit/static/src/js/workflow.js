var get_cookie = function(name) {
    /*
      Retrieve the value of a cookie.
     */
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}



var next_step = function () {
    /*
      This function causes the browser to scroll to the active step.
     */

    var target = $(".active_step:first");
    if (target.length === 0) {
        target = $("input[type='submit']:first");
    }

    if (target[0].scrollIntoView) {
        target[0].scrollIntoView(true);
        
    }
    else {
        $('html, body').animate({
            scrollTop: target.offset().top}, "slow");
    }
};


var update_boxes = function () {
    /* 
       This function is called to ensure that all checkboxes have the
       correct state.
     */
    $(".completed_step input[type='checkbox']").each(
        function (i, checkbox) {
            checkbox.disabled = 1;
            checkbox.checked = 1;
        });

    $(".pending_step input[type='checkbox']").each(
        function (i, checkbox) {
            checkbox.disabled = 1;
            checkbox.checked = 0;
        });

    $(".active_step input[type='checkbox']").each(
        function (i, checkbox) {
            checkbox.disabled = 0;
            checkbox.checked = 0;
        });
};


var check_project_completion = function () {
    /*
      This function checks to see if all steps appear to be completed,
      and updates the submit button accordingly.
     */
    var completed_count = $(".completed_step").length;
    var total_steps = $(".work_step").length;
    var submit_button = $("input[type='submit']")[0];
    if (completed_count == total_steps) {
        submit_button.disabled = 0;
    }
    else {
        submit_button.disabled = 1;
    }
};


var attempt_advance = function () {
    /*
      Called when a checkbox is toggled.  This function checks the
      inputs for the currently active element, and if they are all
      checked, then it changes the class from active to completed, and
      makes an ajax call to create the work receipt.

      If there are pending steps, the first pending step is changed to
      active.

      Then, update_boxes, check_project_completion, and next_step
      should be called again.
     */

    var advance_action = function () {
        var active = $(".active_step");
        active.removeClass("active_step");
        active.addClass("completed_step");        
        var next = $(".pending_step:first");
        if (next) {
            next.removeClass("pending_step");
            next.addClass("active_step");
        }
        update_boxes();
        check_project_completion();
        next_step();
    };

    var checks = $(".active_step input[type='checkbox']");
    var checked = 0;
    for (var i=0; i<checks.length; i+=1) {
        if (checks[i].checked) {
            checked += 1;
        }
    }
    var do_advance = checked === checks.length;

    if (do_advance && checks.length == 1) {
        for (var i=0; i<checks[0].classList.length; i+=1) {
            if (checks[0].classList[i] == "dummy") {
                do_advance = false;
                advance_action();
            }
        }
    }

    if (do_advance) {
        var step_id = $(".active_step .step_id");
        $.ajax({
            url: ohai_data.update_url,
            type: "post",
            data: {
                "step_id": step_id.text(),
            },
            headers: {
                "X-CSRFToken": get_cookie('csrftoken'),
            },
        } );
        advance_action();
    }
};


var resize_steps = function () {
    /*
      Called to fix the height on the steps.
     */
    $(".step_content").height($(window).height()-64);
};

var setup = function () {
    /*
      This function is called on page-load to update various inputs,
      connect events, and finally calls the next_step function.
     */
    resize_steps();
    update_boxes();
    check_project_completion();
    $(".work_step input[type='checkbox']").change(attempt_advance);
    next_step();
};


$(document).ready(setup);
