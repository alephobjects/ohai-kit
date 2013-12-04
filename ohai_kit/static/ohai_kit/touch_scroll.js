

var ohai_scroll = (function() {
    // These variables are relevent to the event.clientX event.clientY
    // coordinates:
    var down_x = 0;
    var down_y = 0;
    var delta_x = 0;
    var delta_y = 0;
    var down_time = 0;

    // The 'origin' variables is the page coordinate which scrolling
    // is relative to:
    var origin_x = 0;
    var origin_y = 0;

    // Inertia should be an integer value between 0 and 100
    //var inertia = 0;

    return {
        scrolling : 0,
        /*
        do_inertia : function () {
            window.setTimeout(
                function () {
                    if (!ohai_scroll.scrolling && inertia > 0) {
                        console.info("inertia: " + inertia);
                        var scroll_x = window.scrollX + delta_x*inertia;
                        var scroll_y = window.scrollY - (delta_y*-inertia);
                        window.scroll(scroll_x, scroll_y);
                        inertia -= .1
                        ohai_scroll.do_inertia();
                    }
                },
                100);
        },*/

        mouse_down_handler : function (event) {
            // There are different coordinates we can use for this,
            // though we only really care about the delta, so any one
            // of them can be used, so long as we're consistent.
            console.info(event);
            down_x = event.clientX;
            down_y = event.clientY;
            origin_x = window.scrollX;
            origin_y = window.scrollY;
            ohai_scroll.scrolling = true;
            down_time = Date.now();
            return false;
        },

        mouse_up_handler : function (event) {
            var dt = Date.now() - down_time;
            var dx = window.scrollX-origin_x;
            var dy = window.scrollY-origin_y;
            var dist = Math.sqrt(dx*dx + dy*dy);
            var speed = dist/dt;
            if (speed > 3) {
                speed = 3;
            }
            inertia = Math.floor(speed/3);
            console.info("speed: "+speed);
            console.info("inertia: " + inertia);
            ohai_scroll.scrolling = false;
            //ohai_scroll.do_inertia();
        },

        mouse_move_handler : function (event) {
            if (ohai_scroll.scrolling) {
                delta_x = event.clientX - down_x;
                delta_y = event.clientY - down_y;               
                window.scroll(origin_x + delta_x, origin_y - delta_y);
                window.getSelection().removeAllRanges()
            }
        },
    };
})();


$(document).mousedown(ohai_scroll.mouse_down_handler);
$(document).mouseup(ohai_scroll.mouse_up_handler);
$(document).mousemove(ohai_scroll.mouse_move_handler);