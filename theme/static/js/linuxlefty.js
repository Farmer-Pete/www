$(document).ready(function() {
    $(".defaultText").focus(function(src) {
        if ($(this).val() == $(this)[0].title) {
            $(this).removeClass("no-data");
            $(this).val("");
        }
    }).blur(function() {
        if ($(this).val() == "") {
            $(this).addClass("no-data");
            $(this).val($(this)[0].title);
        }
    }).addClass("no-data");
    
    $(".defaultText").blur();        

});

$('section.boxes').imagesLoaded( function() {
    $('section.boxes').masonry({
        itemSelector: '.box',
        gutterWidth: 10,
        isResizable: true,
        isAnimated: true,
        animationOptions: {
            duration: 'fast',
            easing: 'linear',
            queue: false
        },
        isFitWidth: true
    });
    doResize();
});

$('section.boxes').infinitescroll({
        loading: {
            finishedMsg: '<em>Bummer, nothing else to read</em>',
            img: SITEURL + '/theme/img/loading.gif',
            msgText: 'Stand by, loading more LinuxLefty goodness...',
            selector: '#scroll_msg'
        },
        itemSelector: 'section.boxes article.box',
        navSelector: 'nav.paginator',
        nextSelector: 'nav.paginator a[rel=next]'
    },
    function( newElements ) {
        var $newElems = $( newElements ).css({ opacity: 0 });
        $newElems.imagesLoaded(function(){
            $newElems.animate({ opacity: 1 });
            $('section.boxes').masonry( 'appended', $newElems, true ); 
        });
    }
);

$('header #logo span.first').css('background-image', 'url(' + SITEURL + '/theme/img/logo' + (Math.floor(Math.random()*16)+1) + '.gif)').delay('slow').imagesLoaded(function() {
    $('header #logo span.second').fadeOut('slow');
});

$('#page > header nav ul li a').mouseenter(function() {
    if ($(this).css('background-color') == 'transparent') {
        $(this).animate({
            'border-bottom-width': '20px',
            'border-top-width': '10px',
            'bottom': '15px'
        });
    }
});

$('#page > header nav ul li.active a').mouseleave(function() {
    if ($(this).css('background-color') == 'transparent') {
        $(this).animate({
            'border-bottom-width': '10px',
            'border-top-width': '20px',
            'bottom': '5px'
        });
    }
});

$('#page > header nav ul li.inactive a').mouseleave(function() {
    if ($(this).css('background-color') == 'transparent') {
        $(this).animate({
            'border-bottom-width': '5px',
            'border-top-width': '0px',
            'bottom': '0px'
        });
    }
});

$('.codehilite').prepend( '<div class="newWindow"><a onclick="javascript:viewCode(this)">View in new window</a></div>' );

function doResize() {
    $('table .codehilite').width($('#content_wrapper').width());
}

function viewCode(target) {
    win = window.open("", "codehilite", "scrollbars=yes");
    win.document.write('<html><head><style>.newWindow { display: none; }</style><body>' + $(target).parents('.codehilite').html() + '</body></html>');
}

$(window).resize(doResize);
