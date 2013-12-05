var next_step = function () {
    /*
      This function causes the browser to scroll to the active step.
     */

    var target = $(".active_step:first");
    if (target.length === 0) {
        target = $("#takemehome");
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


var attempt_advance = function (force) {
    /*
      Called when a checkbox is toggled.  This function checks the
      inputs for the currently active element, and if they are all
      checked, then it changes the class from active to completed.

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
        next_step();
    };


    var checks = $(".active_step input[type='checkbox']");
    if (force) {
        $.map(checks, function(item, index) {
            item.checked = true;
        });
    }

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
    $(".work_step input[type='checkbox']").change(function(){attempt_advance(false)});
    next_step();

    if (!!window.ohai_scroll) {
        // touch screen emulation is enabled, so remove the scroll
        // bar, and attach to the swipe events events.
        ohai_scroll.connect("swipe_left", function(){attempt_advance(true)});
        ohai_scroll.lock_scrolling = true;
    }
};


$(document).ready(setup);
