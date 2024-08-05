document.addEventListener("DOMContentLoaded", function () {
  var togglePasswordBtn2 = document.getElementById("togglePasswordBtn2");
  var password = document.getElementById("password");

  togglePasswordBtn2.addEventListener("click", function () {
    if (password.type === "password") {
      password.type = "text";
      togglePasswordBtn2.innerHTML = '<i class="bi bi-eye-slash-fill"></i>';
    } else {
      password.type = "password";
      togglePasswordBtn2.innerHTML = '<i class="bi bi-eye-fill"></i>';
    }
  });
});

function validarEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

function validaremail() {
  const email = document.getElementById("email").value;
  const emailMessage = document.getElementById("emailMessage");
  const submitBtn = document.getElementById("submitBtn");

  emailMessage.style.display = "none";

  if (email === "") {
    emailMessage.style.display = "none";
  } else if (validarEmail(email)) {
    emailMessage.style.display = "block";
    emailMessage.textContent = "El correo electrónico es válido.";
    emailMessage.className = "errorS";
    setTimeout(function () {
      emailMessage.style.display = "none";
    }, 5000);
  } else {
    emailMessage.style.display = "block";
    emailMessage.textContent = "El correo electrónico no es válido.";
    emailMessage.className = "errorV";
  }

  if (validarEmail(email)) {
  } else {
    submitBtn.setAttribute("disabled", "disabled");
  }
}

function validarContrasenaSegura(password) {
  const regex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  return regex.test(password);
}

function validarContrasenas() {
  const password = document.getElementById("password").value;
  const passwordMessage = document.getElementById("passwordMessage");
  const submitBtn = document.getElementById("submitBtn"); // Obtiene el botón

  passwordMessage.style.display = "none";

  // Validar contraseña segura
  if (password === "") {
    passwordMessage.style.display = "none";
  } else if (validarContrasenaSegura(password)) {
    passwordMessage.style.display = "block";
    passwordMessage.textContent = "La contraseña es segura.";
    passwordMessage.className = "errorS";
    setTimeout(function () {
      passwordMessage.style.display = "none";
    }, 5000);
  } else {
    passwordMessage.style.display = "block";
    passwordMessage.textContent =
      "La contraseña no es segura. Debe tener al menos 8 caracteres, una letra mayúscula, una letra minúscula, un número y un carácter especial(puede ser cualquiera de @$!%*?&).";
    passwordMessage.className = "errorV";
    submitBtn.setAttribute("disabled", "disabled");
  }
}

document.getElementById("email").addEventListener("input", validaremail);
document.getElementById("password").addEventListener("input", validarContrasenas);

//calendario
$(document).ready(function() {
  var fechaMaxima = new Date(); // Obtener la fecha actual
  fechaMaxima.setFullYear(fechaMaxima.getFullYear() - 18); // Restar 18 años a la fecha actual
  $.datepicker.setDefaults($.datepicker.regional["es"]);
  $("#fecha").datepicker({
    inline:true,
    dateFormat: "yy-mm-dd", // Formato de fecha
    onSelect: function(dateText, inst) {
      validarCampos(); // Llama a validarCampos después de seleccionar una fecha
    },
    prevText: "Anterior", // Texto para el botón de mes anterior
    nextText: "Siguiente", // Texto para el botón de mes siguiente
    monthNames: [
      "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ], // Nombres de los meses
    monthNamesShort: [
      "Ene", "Feb", "Mar", "Abr", "May", "Jun",
      "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
    ], // Nombres cortos de los meses
    dayNames: [
      "Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"
    ], // Nombres de los días
    dayNamesMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sá"], // Nombres cortos de los días
    dayNamesShort: ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"], // Nombres abreviados de los días
    onSelect: function(dateText, inst) {
      $(this).val(dateText); // Actualiza el valor del input al seleccionar una fecha
      validarCampos(); // Llama a validarCampos después de seleccionar una fecha
    },
    changeMonth: true, // Habilitar filtro por mes
    changeYear: true, // Habilitar filtro por año
    yearRange: "c-100:c+10", // Mostrar un rango de 100 años hacia atrás y 10 años hacia adelante desde el año actual
    maxDate: fechaMaxima // Establecer la fecha máxima permitida
  });
});

function validarCampos() {
  console.log("ejec");
  var usuario = document.querySelector('input[name="user"]').value;
  var email = document.querySelector('input[name="e-mail"]').value;
  var contraseña = document.querySelector('input[name="contraseña"]').value;
  var sexo = document.querySelector('select[name="sexo"]').value;
  var tipoUsuario = document.querySelector('select[name="Tipo_Usuario"]').value;
  var fecha = document.querySelector('input[name="cumpleaños"]').value;

  // Verificar si todos los campos obligatorios están completos
  if (
    usuario !== "" &&
    email !== "" &&
    contraseña !== "" &&
    sexo !== "" &&
    tipoUsuario !== "" &&
    fecha !== ""
  ) {
    // Si todos los campos están completos, habilitar el checkbox
    console.log("hla");
    document.getElementById("check").disabled = false;
  } else {
    // Si algún campo está vacío, deshabilitar el checkbox
    document.getElementById("check").disabled = true;
  }
}

function activarBoton() {
  var boton = document.getElementById("submitBtn");
  var checkbox = document.getElementById("check");

  // Habilitar el botón si el checkbox está marcado
  boton.disabled = !checkbox.checked;
}

// Agregar evento onchange a los campos para llamar a la función validarCampos() cuando cambien
var campos = document.querySelectorAll(
  ".formulario-registro input, .formulario-registro select"
);
campos.forEach(function (campo) {
  campo.addEventListener("change", validarCampos);
});

// Agregar evento change al checkbox para llamar a la función activarBoton() cuando cambie
document.getElementById("check").addEventListener("change", activarBoton);

//mesajes de error
// Desaparece después de 3 segundos
setTimeout(function () {
  var errorMessage = document.getElementById("error-message");
  errorMessage.style.display = "none";
}, 5000);


