

var ohai_scroll = (function() {
    var down_x = -1;
    var down_y = -1;
    var scrolling = false;

    return {
        mouse_down_handler : function (event) {
            // There are different coordinates we can use for this,
            // though we only really care about the delta, so any one
            // of them can be used, so long as we're consistent.
            down_x = event.pageX;
            down_y = event.pageY;
            scrolling = true;
        },

        mouse_up_handler : function (event) {
            scrolling = false;
        },

        mouse_move_handler : function (event) {
            if (scrolling) {
                var delta_x = event.clientX - down_x;
                var delta_y = event.clientY - down_y;
                window.scroll(delta_x, delta_y*-1);
            }
        },
    };
})();


$(document).mousedown(ohai_scroll.mouse_down_handler);
$(document).mouseup(ohai_scroll.mouse_up_handler);
$(document).mousemove(ohai_scroll.mouse_move_handler);