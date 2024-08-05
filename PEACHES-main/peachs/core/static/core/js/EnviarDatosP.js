$(document).ready(function() {
    // Event listener delegado para los campos de entrada de archivo dentro del formulario con el ID "form"
    $(document).on('change', '#form input[type="file"]', function() {
        // Simular clic en el botón de envío oculto solo si el input de archivo está dentro del formulario
        $(this).closest('form').find('#submit-btn').click();
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var saveButton = document.getElementById("save-button1");
    var hiddenTextInput = document.getElementById("texto1");
    var hiddenSubmitButton = document.getElementById("submit-btn");

    saveButton.addEventListener("click", function() {
        // Obtener el texto del textarea
        var textareaValue = document.getElementById("edit-textarea1").value;

        // Asignar el valor del textarea al input oculto
        hiddenTextInput.value = textareaValue;

        // Hacer clic en el botón de envío oculto
        hiddenSubmitButton.click();
    });
});
document.addEventListener("DOMContentLoaded", function() {
    var saveButton = document.getElementById("save-button3");
    var hiddenTextInput = document.getElementById("texto3");
    var hiddenSubmitButton = document.getElementById("submit-btn");

    saveButton.addEventListener("click", function() {
        // Obtener el texto del textarea
        var textareaValue = document.getElementById("edit-textarea3").value;

        // Asignar el valor del textarea al input oculto
        hiddenTextInput.value = textareaValue;

        // Hacer clic en el botón de envío oculto
        hiddenSubmitButton.click();
    });
});
document.addEventListener("DOMContentLoaded", function() {
    var saveButton = document.getElementById("save-button2");
    var hiddenTextInput = document.getElementById("texto2");
    var hiddenSubmitButton = document.getElementById("submit-btn");

    saveButton.addEventListener("click", function() {
        // Obtener el texto del textarea
        var textareaValue = document.getElementById("edit-textarea2").value;

        // Asignar el valor del textarea al input oculto
        hiddenTextInput.value = textareaValue;

        // Hacer clic en el botón de envío oculto
        hiddenSubmitButton.click();
    });
});
