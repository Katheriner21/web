document.addEventListener("DOMContentLoaded", function () {
  var chatIcon = document.getElementById("chat-icon2");
  var ClosechatIcon = document.getElementById("close-icon-chat2");
  var chatContainer = document.getElementById("chat-container2");

  chatIcon.addEventListener("click", function () {
    chatContainer.style.display = "block";
    chatIcon.style.display = "none";
    console.log('hola')
    var boxMessages = document.querySelector("#boxMessages");
    boxMessages.scrollTop = boxMessages.scrollHeight;
  });

  ClosechatIcon.addEventListener("click", function () {
    chatContainer.style.display = "none";
    chatIcon.style.display = "block";
  });
});

document.querySelector(".botonmas").addEventListener("click", function (event) {
  event.preventDefault();

  // Simular clic en el input para cargar un archivo
  document.querySelector(".subir-h").click();
});

$(document).ready(function () {
  // Event listener para los campos de entrada de archivo
  $('input[type="file"]').change(function () {
    // Simular clic en el botón de envío oculto
    $("#submitbtH").click();
  });
});

function filterHistories(searchText) {
  // Obtener todas las diapositivas del carrusel
  var slides = $(".slick-track").children();

  // Iterar sobre cada diapositiva
  slides.each(function () {
    var slide = $(this);
    var histories = slide.find(".history");
    var shouldShowSlide = false;

    // Iterar sobre cada historia
    histories.each(function () {
      var history = $(this);
      var userName = history.find("p").text().toLowerCase(); // Obtener el nombre de usuario de la historia

      // Si el nombre de usuario contiene el texto de búsqueda, mostrar la diapositiva
      if (userName.includes(searchText.toLowerCase())) {
        shouldShowSlide = true;
        return false; // Salir del bucle de historias
      }
    });

    if (shouldShowSlide) {
      slide.show();
    } else {
      slide.hide();
    }
  });
}
