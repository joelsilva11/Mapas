document.addEventListener('click', function(event) {
    // Lista de sufijos de ID para los dropdowns
    var id_suffixes = ['1', '2','3'];  // Actualiza esta lista con todos los sufijos de ID que estés utilizando

    for (var i = 0; i < id_suffixes.length; i++) {
        var suffix = id_suffixes[i];
        var checklistContainer = document.getElementById('checklist_container-' + suffix);
        var input = document.getElementById('dp-input-' + suffix);
        var button = document.getElementById('dp-button-' + suffix);

        // Si se hace clic en el botón o el input de este dropdown, cambiamos la visibilidad del div
        if (event.target === input || event.target === button) {
            if (checklistContainer.style.display === 'none') {
                checklistContainer.style.display = 'block';
            } else {
                checklistContainer.style.display = 'none';
            }
        }
        // Si se hace clic en cualquier lugar que no sea el div 'checklist_container' o el input/button de este dropdown, ocultamos el div
        else if (!checklistContainer.contains(event.target)) {
            checklistContainer.style.display = 'none';
        }
    }
});

document.addEventListener('click', function(event) {
    // Lista de sufijos de ID para los dropdowns
    var id_suffixes = ['1', '2','3'];  // Actualiza esta lista con todos los sufijos de ID que estés utilizando

    for (var i = 0; i < id_suffixes.length; i++) {
        var suffix = id_suffixes[i];
        var checklistContainer = document.getElementById('tl-container-list-' + suffix);
        var button = document.getElementById('tl-button-' + suffix);
        var icon = document.getElementById('tl-icon-' + suffix);

        // Si se hace clic en el botón o el input de este dropdown, cambiamos la visibilidad del div
        if (event.target === icon ||event.target === button) {
            if (checklistContainer.style.display === 'none') {
                checklistContainer.style.display = 'inline-block';
            } else {
                checklistContainer.style.display = 'none';
            }
        }
        // Si se hace clic en cualquier lugar que no sea el div 'checklist_container' o el input/button de este dropdown, ocultamos el div
        else if (!checklistContainer.contains(event.target)) {
            checklistContainer.style.display = 'none';
        }
    }
});
document.addEventListener('click', function(event) {
    // Lista de sufijos de ID para los dropdowns
    var id_suffixes = ['1', '2','3'];  // Actualiza esta lista con todos los sufijos de ID que estés utilizando

    for (var i = 0; i < id_suffixes.length; i++) {
        var suffix = id_suffixes[i];
        var checklistContainer = document.getElementById('ly-container-list-' + suffix);
        var button = document.getElementById('ly-button-' + suffix);
        var icon = document.getElementById('ly-icon-' + suffix);

        // Si se hace clic en el botón o el input de este dropdown, cambiamos la visibilidad del div
        if (event.target === icon ||event.target === button) {
            if (checklistContainer.style.display === 'none') {
                checklistContainer.style.display = 'inline-block';
            } else {
                checklistContainer.style.display = 'none';
            }
        }
        // Si se hace clic en cualquier lugar que no sea el div 'checklist_container' o el input/button de este dropdown, ocultamos el div
        else if (!checklistContainer.contains(event.target)) {
            checklistContainer.style.display = 'none';
        }
    }
});