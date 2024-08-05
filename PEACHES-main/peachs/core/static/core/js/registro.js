document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.edit-button');
    const popupContainers = document.querySelectorAll('.popup-container');
    const saveButtons = document.querySelectorAll('.save-button');
    const ventana1 = document.querySelectorAll('.ventana1');
    const ventana2 = document.querySelectorAll('.ventana2');
    const ventana3 = document.querySelectorAll('.ventana3');
    const siguiente = document.querySelectorAll('.Siguiente');
    const siguiente2 = document.querySelectorAll('.Siguiente2');
    const ventana4 = document.querySelectorAll('.ventana4');
    const siguiente3 = document.querySelectorAll('.Siguiente3');

    editButtons.forEach((button, index) => {
        button.addEventListener('click', function () {
            popupContainers[index].style.display = 'block';
            ventana1[index].style.display = 'flex';
        });
    });

    siguiente.forEach((button, index) => {
        button.addEventListener('click', function () {
            ventana1[index].style.display = 'none';
            ventana2[index].style.display = 'flex';
        });
    });

    siguiente2.forEach((button, index) => {
        button.addEventListener('click', function () {
            ventana2[index].style.display = 'none';
            ventana3[index].style.display = 'flex';
        });
    });

    siguiente3.forEach((button, index) => {
        button.addEventListener('click', function () {
            ventana3[index].style.display = 'none';
            ventana4[index].style.display = 'flex';
        });
    });

    saveButtons.forEach((button, index) => {
        button.addEventListener('click', function () {
            popupContainers[index].style.display = 'none';
            ventana1[index].style.display = 'none';
            ventana2[index].style.display = 'none';
            ventana3[index].style.display = 'none';
            ventana4[index].style.display = 'none';
        });
    });
});


let campocod = false, campoimg1 = false, campoimg2 = false;
let codigoValidacion;
const checkbox1 = document.getElementById('miCheckbox');
const boton1 = document.getElementById('boton1');
boton1.disabled = true;

checkbox1.addEventListener('change', function () {
    if (checkbox1.checked) {
        boton1.disabled = false; // Habilitar el botón
    } else {
        boton1.disabled = true; // Deshabilitar el botón
    }
});

const checkbox2 = document.getElementById('miCheckbox2');
const boton2 = document.getElementById('boton2');
boton2.disabled = true;

checkbox2.addEventListener('change', function () {
    if (checkbox2.checked) {
        boton2.disabled = false; // Habilitar el botón
    } else {
        boton2.disabled = true; // Deshabilitar el botón
    }
});


function activarEnvio() {
    var formulario = document.getElementById('mi_formulario');
    var botonEnvio = formulario.querySelector('input[type="submit"]');

    botonEnvio.click();
}

function pasarInformacion(origen, destino) {
    var campoOrigen = document.getElementById(origen).value;
    var campoDestino = document.getElementById(destino);
    campoDestino.value = campoOrigen;
}

// Asociar la función al evento de clic del botón
document.getElementById('boton1').addEventListener('click', function () {
    pasarInformacion('nombreO', 'nombreD');
    pasarInformacion('apellidoO', 'apellidoD');
    pasarInformacion('dniO', 'dniD');
    pasarInformacion('telefonoO', 'telefonoD');
    const paragraph = document.getElementById('myParagraph');
    const text = paragraph.textContent;
    sendToServer(text);
});

function sendToServer(user) {
    if (codigoValidacion) {
        // Eliminar el código de validación anterior
        codigoValidacion = undefined;
    }
    // Generar el código de 5 dígitos
    const codigo = Math.floor(10000 + Math.random() * 90000);

    // Guardar el código para su posterior validación
    codigoValidacion = codigo;

    const formData = new FormData();
    formData.append('cod', codigo);
    formData.append('user', user);

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/email/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
        .then(response => {
            if (response.ok) {
                console.log('Datos enviado al servidor');
            } else {
                console.error('Error al enviar el datos al servidor:', response.status);
            }
        })
        .catch(error => {
            console.error('Error de red al enviar el datos al servidor:', error);
        });
}

// Obtén el código de validación almacenado en sessionStorage
const codigoInput = document.getElementById('codigo-input');
const codMessage = document.getElementById("codMessage");
codMessage.style.display = "none";

codigoInput.addEventListener('input', function () {
    const codigoIngresado = codigoInput.value;

    if (codigoInput.value === "") {
        codMessage.style.display = 'none';
    } else if (codigoIngresado === codigoValidacion.toString()) {
        codMessage.style.display = 'block';
        codMessage.textContent = "El codigo es válido.";
        codMessage.className = "errorS";
        setTimeout(function () {
            codMessage.style.display = 'none';
        }, 5000);
        campocod = true
        verificarCamposV2()
    } else {
        codMessage.style.display = 'block';
        codMessage.textContent = "El codigo no es válido.";
        codMessage.className = "errorV";
    }
});

function verificarCampos() {
    const campo1 = document.getElementById('nombreO').value;
    const campo2 = document.getElementById('apellidoO').value;
    const campo3 = document.getElementById('dniO').value;
    const campo4 = document.getElementById('telefonoO').value;
    const checkbox = document.getElementById('miCheckbox');

    if (campo1 !== '' && campo2 !== '' && campo3 !== '' && campo4 !== '') {
        checkbox.disabled = false; // Habilitar checkbox
    } else {
        checkbox.disabled = true; // Deshabilitar checkbox
    }
}

// Agregar el evento 'input' a los campos de entrada
document.getElementById('nombreO').addEventListener('input', verificarCampos);
document.getElementById('apellidoO').addEventListener('input', verificarCampos);
document.getElementById('dniO').addEventListener('input', verificarCampos);
document.getElementById('telefonoO').addEventListener('input', verificarCampos);

// Verificar campos al cargar la página
verificarCampos();


//camara fotos
const perfilCamera = document.getElementById('perfilCamera');
const frenteCamera = document.getElementById('frenteCamera');

perfilCamera.addEventListener('click', function () {
    startCamera1(perfilCamera);
});

frenteCamera.addEventListener('click', function () {
    startCamera2(frenteCamera);
});

function startCamera1(cameraElement) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            cameraElement.innerHTML = '';
            const video = document.createElement('video');
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');

            video.autoplay = true;
            video.srcObject = stream;
            cameraElement.appendChild(video);

            // Icono de cámara
            const cameraIcon = document.createElement('span');
            cameraIcon.classList.add('bi', 'bi-camera-fill', 'camera-icon');
            cameraElement.appendChild(cameraIcon);

            // Capturar foto al hacer clic en el video
            cameraIcon.addEventListener('click', function () {
                perfilCamera.style.display = 'none';

                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                context.drawImage(video, 0, 0, canvas.width, canvas.height);

                const image = new Image();
                image.onload = function () {
                    cameraElement.innerHTML = '';
                    cameraElement.appendChild(image);
                    // Mostrar imagen tomada en el div "imagenTomada"
                    const imagenTomadaDiv = document.getElementById('imagenTomada');
                    imagenTomadaDiv.style.display = 'block';
                    imagenTomadaDiv.innerHTML = '';
                    imagenTomadaDiv.appendChild(image);
                    // Dentro del evento click del icono de la cámara
                    const repeatButton = document.createElement('button');
                    repeatButton.classList.add('bi', 'bi-arrow-counterclockwise', 'repeat-button');
                    imagenTomadaDiv.appendChild(repeatButton);
                    // Manejador de eventos para el botón de repetición
                    repeatButton.addEventListener('click', function () {
                        // Restablecer la interfaz de la cámara
                        imagenTomadaDiv.style.display = 'none';
                        perfilCamera.style.display = 'block';
                        video.play();
                    });
                };
                image.src = canvas.toDataURL('image/png');
                const paragraph = document.getElementById('myParagraph');
                const text = paragraph.textContent;
                sendImageToServer(image, text, 1);
                campoimg1 = true
                verificarCamposV2()
            });
        })
        .catch(function (error) {
            console.log('Error al acceder a la cámara: ', error);
        });
}

function startCamera2(cameraElement) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            cameraElement.innerHTML = '';
            const video = document.createElement('video');
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');

            video.autoplay = true;
            video.srcObject = stream;
            cameraElement.appendChild(video);

            // Icono de cámara
            const cameraIcon = document.createElement('span');
            cameraIcon.classList.add('bi', 'bi-camera-fill', 'camera-icon');
            cameraElement.appendChild(cameraIcon);

            // Capturar foto al hacer clic en el video
            cameraIcon.addEventListener('click', function () {
                frenteCamera.style.display = 'none';

                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                context.drawImage(video, 0, 0, canvas.width, canvas.height);

                const image = new Image();
                image.onload = function () {
                    cameraElement.innerHTML = '';
                    cameraElement.appendChild(image);
                    // Mostrar imagen tomada en el div "imagenTomada"
                    const imagenTomadaDiv = document.getElementById('imagenTomada2');
                    imagenTomadaDiv.style.display = 'block';
                    imagenTomadaDiv.innerHTML = '';
                    imagenTomadaDiv.appendChild(image);
                    // Dentro del evento click del icono de la cámara
                    const repeatButton = document.createElement('button');
                    repeatButton.classList.add('bi', 'bi-arrow-counterclockwise', 'repeat-button');
                    imagenTomadaDiv.appendChild(repeatButton);
                    // Manejador de eventos para el botón de repetición
                    repeatButton.addEventListener('click', function () {
                        // Restablecer la interfaz de la cámara
                        imagenTomadaDiv.style.display = 'none';
                        frenteCamera.style.display = 'block';
                        video.play();
                    });
                };
                image.src = canvas.toDataURL('image/png');
                const paragraph = document.getElementById('myParagraph');
                const text = paragraph.textContent;
                sendImageToServer(image, text, 2);
                campoimg2 = true
                verificarCamposV2()
            });
        })
        .catch(function (error) {
            console.log('Error al acceder a la cámara: ', error);
        });
}

function sendImageToServer(image, dato, num) {
    // Convertir la imagen en un archivo binario
    const blob = dataURItoBlob(image.src);

    // Crear un objeto FormData y agregar el archivo binario
    const formData = new FormData();
    formData.append('image', blob, 'image.png');
    formData.append('dato', dato);
    formData.append('num', num);

    // Obtener el token CSRF
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Enviar la solicitud al servidor
    fetch('/upload-images/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
        .then(response => {
            if (response.ok) {
                console.log('Imagen enviada correctamente.');
            } else {
                console.error('Error al enviar la imagen al servidor.');
            }
        })
        .catch(error => {
            console.error('Error al enviar la imagen al servidor:', error);
        });
}

function dataURItoBlob(dataURI) {
    // Convertir la cadena base64 en una matriz de bytes
    const byteString = atob(dataURI.split(',')[1]);

    // Crear un ArrayBuffer y un Uint8Array para los datos binarios
    const buffer = new ArrayBuffer(byteString.length);
    const array = new Uint8Array(buffer);

    // Llenar el Uint8Array con los datos binarios
    for (let i = 0; i < byteString.length; i++) {
        array[i] = byteString.charCodeAt(i);
    }

    // Crear un objeto Blob a partir de los datos binarios
    const blob = new Blob([array], { type: 'image/png' });
    return blob;
}

const checkbox = document.getElementById('miCheckbox2');
function verificarCamposV2() {
    if (campocod && campoimg1 && campoimg2) {
        checkbox.disabled = false; // Habilitar checkbox
    } else {
        checkbox.disabled = true; // Deshabilitar checkbox
    }
}

