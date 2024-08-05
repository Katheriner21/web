document.addEventListener('DOMContentLoaded', function() {
  const editButtons = document.querySelectorAll('.botonopinion');
  const popupContainers = document.querySelectorAll('.popup-container');
  const saveButtons = document.querySelectorAll('.save-butto');
  const editTextareas = document.querySelectorAll('.edit-textarea');
  const close = document.querySelectorAll('.close-ico');

  editButtons.forEach((button, index) => {
      button.addEventListener('click', function() {
        popupContainers[index].style.display = 'flex';
      });
  });

  close.forEach((button, index) => {
    button.addEventListener('click', function(){
      popupContainers[index].style.display = 'none';
    });
  });

  saveButtons.forEach((button, index) => {
      button.addEventListener('click', function() {
          popupContainers[index].style.display = 'none';
          var opinion = editTextareas[index].value;
          console.log(opinion)
          enviarOpinion(opinion);
      });
  });
});

function enviarOpinion(opinion) {
  // Enviar la opinión al servidor
  var formData = new FormData();
  formData.append('opinion', opinion);

  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  fetch('/cargar_op/', {
      method: 'POST',
      headers: {
          'X-CSRFToken': csrfToken  // Asegúrate de incluir el token CSRF
      },
      body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.hasOwnProperty('error')) {
      var mensajeContainer = document.getElementById('error-messages');
      mensajeContainer.style.display = "block";
      mensajeContainer.innerHTML = '<p>' + data.error + '</p>';
      mensajeContainer.classList.remove('success');
      mensajeContainer.classList.add('error');
    } else if (data.hasOwnProperty('message')) {
      var mensajeContainer = document.getElementById('error-messages');
      mensajeContainer.style.display = "block";
      mensajeContainer.innerHTML = '<p>' + data.message + '</p>';
      mensajeContainer.classList.remove('error');
      mensajeContainer.classList.add('success');
    }
    setTimeout(function () {
      mensajeContainer.style.display = 'none';
      window.location.reload();
    }, 5000);
  })
  .catch(error => {
      console.error('Error al enviar la opinión:', error);
      var mensajeContainer = document.getElementById('error-messages');
      mensajeContainer.style.display = "block";
      mensajeContainer.innerHTML = '<p>Hubo un error al enviar la opinión. Por favor, inténtalo de nuevo.</p>';
      mensajeContainer.classList.remove('success');
      mensajeContainer.classList.add('error');
      setTimeout(function () {
        mensajeContainer.style.display = 'none';
        window.location.reload();
      }, 5000);
  });
}

//mesajes de error
// Obtén el contenedor del mensaje de error
var errorMessage = document.getElementById('error-message');

// Muestra el mensaje de error
errorMessage.style.display = 'block';

// Desaparece después de 3 segundos
setTimeout(function () {
  errorMessage.style.display = 'none';
}, 5000);
