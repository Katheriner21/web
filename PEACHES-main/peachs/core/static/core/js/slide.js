$(document).ready(function () {
    $('.carouselh').slick({
        slidesToShow: 8, // Muestra 4 imágenes a la vez
        slidesToScroll: 1, // Se desplaza 1 imagen a la vez
        dots: false, // Muestra los puntos de navegación
        arrows: false, // botones
        infinite: true, // Permite un desplazamiento infinito
        autoplay: false, // Inicia la reproducción automática
        draggable: true,
        swipe: true, // Habilita el desplazamiento al deslizar
        ipeToSlide: true, // Permite desplazarse directamente a la diapositiva más cercana al deslizar
        swipeThreshold: 70, // Ajusta la distancia necesaria para activar el desplazamiento
        responsive: [
            {
                breakpoint: 768, // Cambios en la configuración en dispositivos con ancho de pantalla <= 768px
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 480, // Cambios en la configuración en dispositivos con ancho de pantalla <= 480px
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 325, // Cambios en la configuración en dispositivos con ancho de pantalla <= 480px
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                }
            }
        ]
    });
});
$(document).ready(function () {
    $('.carouselh2').slick({
        slidesToShow: 7, // Muestra 4 imágenes a la vez
        slidesToScroll: 1, // Se desplaza 1 imagen a la vez
        dots: false, // Muestra los puntos de navegación
        arrows: false, // botones
        infinite: false, // Permite un desplazamiento infinito
        autoplay: false, // Inicia la reproducción automática
        draggable: true,
        swipe: true, // Habilita el desplazamiento al deslizar
        ipeToSlide: true, // Permite desplazarse directamente a la diapositiva más cercana al deslizar
        swipeThreshold: 70, // Ajusta la distancia necesaria para activar el desplazamiento
        responsive: [
            {
                breakpoint: 768, // Cambios en la configuración en dispositivos con ancho de pantalla <= 768px
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 480, // Cambios en la configuración en dispositivos con ancho de pantalla <= 480px
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                }
            }
        ]
    });
});


$(document).ready(function () {
    $('.opiniones').slick({
        slidesToShow: 3, // Muestra 4 imágenes a la vez
        slidesToScroll: 1, // Se desplaza 1 imagen a la vez
        dots: false, // Muestra los puntos de navegación
        arrows: false, // botones
        infinite: true, // Permite un desplazamiento infinito
        autoplay: true, // Inicia la reproducción automática
        draggable: true,
        swipe: true, // Habilita el desplazamiento al deslizar
        ipeToSlide: true, // Permite desplazarse directamente a la diapositiva más cercana al deslizar
        swipeThreshold: 70, // Ajusta la distancia necesaria para activar el desplazamiento
        prevArrow: '<button type="button" class="slick-prev"><i class="carousel-control-prev-icon"></i></button>',
        nextArrow: '<button type="button" class="slick-next"><i class="carousel-control-next-icon"></i></button>',
        responsive: [
            {
                breakpoint: 768, // Cambios en la configuración en dispositivos con ancho de pantalla <= 768px
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 480, // Cambios en la configuración en dispositivos con ancho de pantalla <= 480px
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 325, // Cambios en la configuración en dispositivos con ancho de pantalla <= 480px
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                }
            }
        ]
    });
});

