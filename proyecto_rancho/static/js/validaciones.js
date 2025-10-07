$(document).ready(function(){
    // Registrar consumo
    $('#registroSubmit').on('click', function(event){
        event.preventDefault();
        const seleccionados = $('input[name="comida"]:checked');
        if (seleccionados.length === 0) {
            $('#smallComida').text('Debe seleccionar una o más comidas');
        } else {
            $('#registroForm').submit(); // solo se envía si está correcto
        }
    });

    // Crear usuario
    $('#crearUsuarioSubmit').on('click', function(event){
    event.preventDefault();

    const campos = [
        {id: '#first_name', mensaje: 'El nombre es obligatorio', small: '#smallFirstName'},
        {id: '#last_name', mensaje: 'El apellido es obligatorio', small: '#smallLastName'},
        {id: '#dni', mensaje: 'El documento es obligatorio', small: '#smallDni'},
        {id: '#casinoSelect', mensaje: 'Debe selecionar un casino', small: '#smallCasino'},
        {id: '#username', mensaje: 'El nombre de usuario es obligatorio', small: '#smallUsername'}
    ];

    let formularioValido = true;

    // Validación de campos obligatorios
    campos.forEach(campo => {
        const valor = $(campo.id).val();
        if (!valor) {
            $(campo.small).text(campo.mensaje);
            $(campo.id).addClass('is-invalid');
            formularioValido = false;
        } else {
            $(campo.small).text('');
            $(campo.id).removeClass('is-invalid');
        }
    });

    // Validación de contraseñas
    const password1 = $('#password').val();
    const password2 = $('#password2').val();

    if (!password1 || !password2 || password1 != password2) {
        $('#smallPassword').text('Las contraseñas no coinciden');
        $('#password, #password2').addClass('is-invalid');
        formularioValido = false;
    } else {
        $('#smallPassword').text('');
        $('#password, #password2').removeClass('is-invalid');
    }

    // Enviar formulario si todo está bien
    if (formularioValido) {
        $('#crearUsuarioForm').submit();
    }
}); 
})