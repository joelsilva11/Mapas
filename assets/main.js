document.addEventListener('click', function(event) {
    var checklistContainer = document.getElementById('checklist_container');
    var kdeButton = document.getElementById('kde-button');

    // Si se hace clic en el botón 'kde-button', cambiamos la visibilidad del div
    if (event.target === kdeButton) {
        if (checklistContainer.style.display === 'none') {
            checklistContainer.style.display = 'block';
        } else {
            checklistContainer.style.display = 'none';
        }
    }
    // Si se hace clic en cualquier lugar que no sea el div 'checklist_container' o el botón 'kde-button', ocultamos el div
    else if (!checklistContainer.contains(event.target)) {
        checklistContainer.style.display = 'none';
    }
});
