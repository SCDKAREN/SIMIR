$('#btnActivar').on('click', async function() {
    const url = $(this).data('url'); // 
    csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const response = await fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken }, 
    });

    const data = await response.json();
    if (data.success) {
        $(this).attr('disabled', true);
        $(this).data('activado', true);
        $(this).addClass('btn-secondary').removeClass('btn-warning');
        $(this).text("El formulario está activo hasta las " + data.expira);
    } else {
        alert("❌ " + (data.message || "No se pudo activar el formulario."));
    }
});