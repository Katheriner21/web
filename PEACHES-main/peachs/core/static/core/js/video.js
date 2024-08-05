let videoPreview = document.getElementById('videoPreview');
let videoImg = document.getElementById('video-img');
let viewrecord = document.getElementById('viewrecord');
let startRecordingButton = document.getElementById('startRecording');
let stopRecordingButton = document.getElementById('stopRecording');
let guardar =  document.getElementById('grdS3');
guardar.disabled = true;
const paragraph = document.getElementById('myParagraph');
const text = paragraph.textContent;
let mediaRecorder;
let recordedChunks = [];

function startRecordingWithCountdown() {
    var count = 5; // Número de segundos para el conteo
    var countdownElement = document.getElementById('countdown');
    countdownElement.style.display = 'block';

    // Muestra el contador antes de comenzar la grabación
    countdownElement.textContent = count;

    var countdownInterval = setInterval(function() {
        if (count > 0) {
            count--;
            countdownElement.textContent = count;
        } else {
            clearInterval(countdownInterval);
            startRecording();
            countdownElement.style.display = 'none';
        }
    }, 1000);
}

startRecordingButton.addEventListener('click', startRecordingWithCountdown);
stopRecordingButton.addEventListener('click', startRecordingWithCountdown);


function startRecording() {
    videoImg.style.display = "none";
    videoPreview.style.display = "block";
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            videoPreview.srcObject = stream;
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                recordedChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                let recordedBlob = new Blob(recordedChunks, { type: 'video/webm' });
                recordedChunks = [];

                sendVideoToServer(recordedBlob,text);

                // Mostrar la grabación en el elemento de video
                viewrecord.src = URL.createObjectURL(recordedBlob);
                viewrecord.style.display = "block";
                videoPreview.style.display = "none";
                stopRecordingButton.style.display = "block";
                startRecordingButton.style.display = "none";

                // Habilitar el botón de inicio de grabación nuevamente
                startRecordingButton.disabled = false;
                stopRecordingButton.disabled = false;
                guardar.disabled = false;
            };

            mediaRecorder.start();
            startRecordingButton.disabled = true;
            stopRecordingButton.disabled = true;
            guardar.disabled = true;
            viewrecord.style.display = "none";
            videoPreview.style.display = "block";



            // Detener la grabación después de 15 segundos
            setTimeout(() => {
                stopRecording();
            }, 15000);
        })
        .catch(error => {
            console.error('Error al acceder a la cámara:', error);
        });
}

function stopRecording() {
    mediaRecorder.stop();
}

function sendVideoToServer(videoBlob, dato) {
    const formData = new FormData();
    formData.append('video', videoBlob);
    formData.append('dato', dato);

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/upload-video/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            console.log('Video enviado al servidor');
            // Realizar acciones adicionales después de enviar el video correctamente
        } else {
            console.error('Error al enviar el video al servidor:', response.status);
            // Realizar acciones adicionales en caso de error
        }
    })
    .catch(error => {
        console.error('Error de red al enviar el video al servidor:', error);
        // Realizar acciones adicionales en caso de error de red
    });
}