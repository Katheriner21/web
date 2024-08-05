document.addEventListener("DOMContentLoaded", function () {
  const aggpub = document.querySelectorAll(".agg-img");
  const editpub = document.querySelectorAll(".edit");
  const popupContainers = document.querySelectorAll(".cont1");
  cont = document.getElementById("cont2");
  const saveButtons = document.querySelectorAll(".save");
  const editButtons = document.querySelectorAll(".editar");
  const close = document.querySelectorAll(".close-pub");
  const close2 = document.querySelectorAll(".cls2");
  const pub = document.querySelectorAll(".input-pub");
  const info = document.querySelectorAll(".input-info");
  const pub2 = document.querySelectorAll(".input-pub2");
  const info2 = document.querySelectorAll(".input-info2");
  var id = 0;

  aggpub.forEach((button, index) => {
    button.addEventListener("click", function () {
      popupContainers[index].style.display = "block";
    });
  });

  editpub.forEach((button, index) => {
    button.addEventListener("click", function () {
      event.preventDefault();
      cont.style.display = "block";
      id = editpub[index].getAttribute("data-id");
    });
  });

  close.forEach((button, index) => {
    button.addEventListener("click", function () {
      popupContainers[index].style.display = "none";
    });
  });

  close2.forEach((button, index) => {
    button.addEventListener("click", function () {
      cont.style.display = "none";
    });
  });

  saveButtons.forEach((button, index) => {
    button.addEventListener("click", function () {
      popupContainers[index].style.display = "none";
      var p = pub[index].files[0];
      var i = info[index].value;
      enviarPub(p, i);
    });
  });

  editButtons.forEach((button, index) => {
    button.addEventListener("click", function () {
      cont.style.display = "none";
      var p = pub2[index].files[0];
      var i = info2[index].value;
      editarPub(p, i, id);
    });
  });
});

var dropArea = document.getElementById("dropArea");
var fileInput = document.getElementById("fileInput");
var dropArea2 = document.getElementById("dropArea2");
var fileInput2 = document.getElementById("fileInput2");

// Agrega eventos para evitar que el navegador abra el archivo al arrastrarlo
["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
  dropArea.addEventListener(eventName, preventDefaults, false);
});
["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
  dropArea2.addEventListener(eventName, preventDefaults, false);
});

// Resalta el área de soltar cuando se arrastra un archivo sobre ella
["dragenter", "dragover"].forEach((eventName) => {
  dropArea.addEventListener(eventName, highlight, false);
});
["dragenter", "dragover"].forEach((eventName) => {
  dropArea2.addEventListener(eventName, highlight2, false);
});

// Quita el resaltado cuando el archivo se deja de arrastrar
["dragleave", "drop"].forEach((eventName) => {
  dropArea2.addEventListener(eventName, unhighlight2, false);
});
["dragleave", "drop"].forEach((eventName) => {
  dropArea.addEventListener(eventName, unhighlight, false);
});

// Procesa el archivo cuando se suelta en el área de soltar
dropArea.addEventListener("drop", handleDrop, false);
dropArea2.addEventListener("drop", handleDrop2, false);

// Prevención de acciones por defecto
function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}


// Resalta el área de soltar
function highlight(e) {
  dropArea.classList.add("highlight");
}
function highlight2(e) {
  dropArea2.classList.add("highlight2");
}

// Quita el resaltado del área de soltar
function unhighlight(e) {
  dropArea.classList.remove("highlight");
}
function unhighlight2(e) {
  dropArea2.classList.remove("highlight2");
}

// Maneja la carga de archivos cuando se suelta en el área de soltar
function handleDrop(e) {
  var dt = e.dataTransfer;
  var files = dt.files;
  fileInput.files = files;
  handleFiles(files);
}

function handleDrop2(e) {
  var dt = e.dataTransfer;
  var files = dt.files;
  fileInput2.files = files;
  handleFiles2(files);
}

// Procesa los archivos
function handleFiles2(files) {
  files = [...files];
  files.forEach(uploadFile2);
}
function handleFiles(files) {
  files = [...files];
  files.forEach(uploadFile);
}

// Sube el archivo
function uploadFile2(file) {
  var reader = new FileReader();

  reader.onload = function (e) {
    var fileType = file.type.split("/")[0];
    if (fileType === "image") {
      var img = new Image();
      img.src = e.target.result;
      img.style.maxWidth = "100%";
      img.style.maxHeight = "100%";
      dropArea2.innerHTML = "";
      dropArea2.appendChild(img);
    } else if (fileType === "video") {
      var video = document.createElement("video");
      video.controls = true;
      video.style.maxWidth = "100%";
      video.style.maxHeight = "100%";
      var source = document.createElement("source");
      source.src = e.target.result;
      source.type = file.type;
      video.appendChild(source);
      dropArea2.innerHTML = "";
      dropArea2.appendChild(video);
    }
  };

  reader.readAsDataURL(file);
}

function uploadFile(file) {
  var reader = new FileReader();

  reader.onload = function (e) {
    var fileType = file.type.split("/")[0];
    if (fileType === "image") {
      var img = new Image();
      img.src = e.target.result;
      img.style.maxWidth = "100%";
      img.style.maxHeight = "100%";
      dropArea.innerHTML = "";
      dropArea.appendChild(img);
    } else if (fileType === "video") {
      var video = document.createElement("video");
      video.controls = true;
      video.style.maxWidth = "100%";
      video.style.maxHeight = "100%";
      var source = document.createElement("source");
      source.src = e.target.result;
      source.type = file.type;
      video.appendChild(source);
      dropArea.innerHTML = "";
      dropArea.appendChild(video);
    }
  };

  reader.readAsDataURL(file);
}

// Abre el cuadro de diálogo de selección de archivos al hacer clic en el área de soltar
dropArea.addEventListener("click", () => {
  fileInput.click();
});

// Procesa los archivos seleccionados desde el cuadro de diálogo de selección de archivos
fileInput.addEventListener("change", () => {
  handleFiles(fileInput.files);
});

// Abre el cuadro de diálogo de selección de archivos al hacer clic en el área de soltar
dropArea2.addEventListener("click", () => {
  fileInput2.click();
});

// Procesa los archivos seleccionados desde el cuadro de diálogo de selección de archivos
fileInput2.addEventListener("change", () => {
  handleFiles2(fileInput2.files);
});

function enviarPub(pub, info) {
  // Enviar la opinión al servidor
  var formData = new FormData();
  formData.append("pub", pub);
  formData.append("info", info);

  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  fetch("/cargar_pub/", {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken, // Asegúrate de incluir el token CSRF
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Si la publicación se guardó correctamente, redirigir a la URL especificada
        window.location.href = data.redirect_url;
      } else {
          // Manejar el caso de error aquí
          console.error("Error al guardar la publicación:", data.error);
      }
    })
    .catch((error) => {
      console.error("Error al enviar la publicación:", error);
    });
}

function editarPub(pub, info, id) {
  // Enviar la opinión al servidor
  var formData = new FormData();
  formData.append("id",id);
  formData.append("pub", pub);
  formData.append("info", info);

  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  fetch("/editar_pub/", {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken, // Asegúrate de incluir el token CSRF
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Si la publicación se guardó correctamente, redirigir a la URL especificada
        window.location.href = data.redirect_url;
      } else {
          // Manejar el caso de error aquí
          console.error("Error al guardar la publicación:", data.error);
      }
    })
    .catch((error) => {
      console.error("Error al enviar la publicación:", error);
    });
}
