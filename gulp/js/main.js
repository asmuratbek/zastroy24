//
// Подключение библиотек
//
// --------------------------------------------

//= jquery/jquery.js
//= slick/slick.min.js
//= nouislider/nouislider.js
//= jquery.easy-autocomplete/jquery.easy-autocomplete.js
//= uikit/uikit.min.js
//= uikit/uikit-icons.js


$(document).ready(function () {
    var slider_for = $('.slider-for');
    var slider_nav = $('.slider-nav');
    var slider_product = $('.slider-product');


    if (slider_for !== undefined && slider_for !== null) {
        slider_for.slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false,
            fade: true,
            asNavFor: '.slider-nav'
        });
    }
    if (slider_nav !== undefined && slider_nav !== null) {
        slider_nav.slick({
            slidesToShow: 4,
            slidesToScroll: 1,
            asNavFor: '.slider-for',
            dots: false,
            centerMode: true,
            focusOnSelect: true
        });
    }
    if (slider_product !== undefined && slider_product !== null) {
        slider_product.slick({
            dots: false,
            lazyLoad: 'ondemand',
            infinite: true,
            speed: 900,
            slidesToShow: 4,
            slidesToScroll: 4,
            nextArrow: '<span class="slick-next" uk-icon="icon: chevron-right; ratio: 2"></span>',
            prevArrow: '<span class="slick-prev" uk-icon="icon: chevron-left; ratio: 2"></span>',
            responsive: [
                {
                    breakpoint: 1336,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 3
                    }
                },
                {
                    breakpoint: 960,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 2
                    }
                },
                {
                    breakpoint: 640,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1
                    }
                }

            ]
        });
    }
});

