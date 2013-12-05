

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
        prevent_links : false,
        scrolling : 0,

        mouse_down_handler : function (event) {
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
            var scroll_x = window.scrollX-origin_x;
            var scroll_y = window.scrollY-origin_y;


            ohai_scroll.scrolling = false;
            window.setTimeout(function () {
                ohai_scroll.prevent_links = false;
            }, 100);
        },

        mouse_move_handler : function (event) {
            if (ohai_scroll.scrolling) {
                delta_x = event.clientX - down_x;
                delta_y = event.clientY - down_y;               
                window.scroll(origin_x + delta_x, origin_y - delta_y);
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