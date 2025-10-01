$(document).ready(function(){
    
    optional_config = {
        altInput: true,
        altFormat: "j \\d\\e F \\d\\e Y",
        dateFormat: "Y-m-d",
        locale: "es",
        defaultDate: "today",
    }

    $("#filtroFecha").flatpickr(optional_config);

})