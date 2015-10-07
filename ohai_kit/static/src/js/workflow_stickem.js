(function() {

  $(document).ready(function() {

    var $content = $('#content_area');

    $content.imagesLoaded()
      .done( function( instance ) {

        // Run stickem after images loaded, to get accurate heights.
        $content.stickem({
          item: '.text_column',
          container: '.work_step'
        });
      });
  });

})();