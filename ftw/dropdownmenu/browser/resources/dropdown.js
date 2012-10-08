jQuery(document).ready(function($) {
    var numColumns = 3;

    var colWidth = $('#portal-globalnav .navTreeLevel0 > .navTreeItem').first().width();
    var totalWidth = colWidth * numColumns;

    $('#portal-globalnav > li').each(function(index, elem) {

        // show element for height calculation
        $(elem).children('ul').show();

        // calculate heights of top-level elements
        var heights = new Array();
        var totalHeight = 0;
        $(elem).find('.navTreeLevel0 > .navTreeItem').each(function(i, e) {
            heights[i] = $(e).height();
            totalHeight += heights[i];
        });

        // hide element
        $(elem).children('ul').hide();

        // distribute top-level elements in columns
        var cumHeight = 0;
        var colHeight = totalHeight / numColumns;
        var colNumber = 0;
        $(elem).find('.navTreeLevel0 > .navTreeItem').each(function(i, e) {
            cumHeight += heights[i];
            $(e).addClass('col' + colNumber);
            if (cumHeight >= colHeight) {
                cumHeight = 0;
                colNumber += 1;
            }
        });
        for (i=0; i<numColumns; i++) {
            $(elem).find('li.col' + i).wrapAll('<li class="navTreeColumn colum' + i + '"><ul /></li>');
        }

        // set witdh
        $(elem).find('.navTreeLevel0').css('width', totalWidth + 'px');

    });


    // show dropdown on hover
    $("#portal-globalnav > li").hoverIntent(
        function() {
            $(this).children('.navTreeLevel0').show(10);
        }, function() {
            $(this).children('.navTreeLevel0').hide(100);
        }
    ).click(
        function() {
            $(this).parent().find('.navTreeLevel0').hide(0);
        }
    );
    
});
