function setupImageInput(iconClass, inputClass) {
    // Manejar clic en el icono
    document.querySelector(iconClass).addEventListener('click', function() {
        document.querySelector(inputClass).click();
    });
}

// Configurar la carga de imagen para cada conjunto de elementos
setupImageInput('.icono-perfil', '.input-perfil');
setupImageInput('.icono-portada', '.input-portada');

document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.edit-button');
    const popupContainers = document.querySelectorAll('.popup-container');
    const saveButtons = document.querySelectorAll('.save-button');
    const editTextareas = document.querySelectorAll('.edit-textarea');
    const codeTexts = document.querySelectorAll('.code-text');

    editButtons.forEach((button, index) => {
        button.addEventListener('click', function() {
            popupContainers[index].style.display = 'block';
            editTextareas[index].value = codeTexts[index].textContent.trim();
        });
    });

    saveButtons.forEach((button, index) => {
        button.addEventListener('click', function() {
            codeTexts[index].textContent = editTextareas[index].value;
            popupContainers[index].style.display = 'none';
        });
    });
});
