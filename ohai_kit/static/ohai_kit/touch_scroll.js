

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

    var signals = {
        swipe_left : [
            function () {
                console.info("swipe left");
            },
        ],

        swipe_right : [
            function () {
                console.info("swipe right");
            },
        ],
    };

    var trigger_signal = function (signal_name) {
        /*
          Trigger_signal(signal_name) is used to schedule immediate
          timeouts for all handlers associated to the named signal.

          Timeouts are used so that if the handler has an error, it
          won't break touch screen emulation.
         */
        $.map(signals[signal_name], function (item, index) {
            setTimeout(item, 0);
        });
    };

    return {
        prevent_links : false,
        lock_scrolling : false,
        scrolling : 0,

        connect : function (name, handler) {
            /* Adds a signal handler. */
            signals[name].push(handler);
        },

        mouse_down_handler : function (event) {
            down_x = event.clientX;
            down_y = event.clientY;
            origin_x = window.scrollX;
            origin_y = window.scrollY;
            // Reset the deltas, clicks following a swipe event don't
            // also trigger additional swipe events:
            delta_x = 0;
            delta_y = 0;
            ohai_scroll.scrolling = true;
            down_time = Date.now();
            return false;
        },

        mouse_up_handler : function (event) {
            ohai_scroll.scrolling = false;
            var scroll_x = window.scrollX-origin_x;
            var scroll_y = window.scrollY-origin_y;
            var swipe_min = $(document).width()/4;
            var max_scroll = $(document).height()/30;
            setTimeout(function () {
                ohai_scroll.prevent_links = false;
            }, 100);
            // check for horizontal swipe gestures
            if (Math.abs(delta_x) > swipe_min && scroll_x == 0 && scroll_y < max_scroll) {
                if (delta_x < 0) {
                    trigger_signal("swipe_left");
                }
                else {
                    trigger_signal("swipe_right");
                }
            }
        },

        mouse_move_handler : function (event) {
            if (ohai_scroll.scrolling) {
                delta_x = event.clientX - down_x;
                delta_y = event.clientY - down_y;
                if (!ohai_scroll.lock_scrolling) {
                    window.scroll(origin_x + delta_x, origin_y - delta_y);
                }
                window.getSelection().removeAllRanges()
                var dt = Date.now() - down_time;
                if (dt > 100) {
                    ohai_scroll.prevent_links = true;
                }
            }
        },
    };
})();


$(document).mousedown(ohai_scroll.mouse_down_handler);
$(document).mouseup(ohai_scroll.mouse_up_handler);
$(document).mousemove(ohai_scroll.mouse_move_handler);


$(document).ready(function () {
    $("a").click(function (event) {
        if (ohai_scroll.prevent_links) {
            console.info("blocked link");
            event.preventDefault();
            event.stopPropagation()
            return false;
        }
    });
});