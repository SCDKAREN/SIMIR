
let idRowClicked;
$(document).ready(function () {
    
    const url = $('#registroTable').data('url');
    dataTable = $('#registroTable').DataTable({
        processing: true,
        serverSide: true,
        // dom: 'Bfrtip',
        // buttons: [
        //     {
        //         extend: 'excelHtml5',
        //         text: '📊 Excel',
        //         className: 'btn btn-success'
        //     },
        //     {
        //         extend: 'pdfHtml5',
        //         text: '📄 PDF',
        //         className: 'btn btn-danger'
        //     }
        // ],
        ajax: {
            url: url,  // Ruta a tu vista de servidor
            data: function (d) {
                d.comida = $('#filtroComida').val();
                d.casino = $('#filtroCasino').val();
                d.fecha = $('#filtroFecha').val();
            },
            dataSrc: 'data'       // nombre del campo que contiene la lista de alarmas
        },
        columns: [
            { 
                data: 'fecha_hora',
                render: function (data, type, row) {
                    const date = new Date(data);
                    const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' };
                    return date.toLocaleDateString('es-ES', options).replace(',', '');
                }
            },
            { data: 'apellido' },
            { data: 'nombre' },            
            { data: 'documento' },
            { data: 'casino' },
            { data: 'comida',
                render:function(data,type,row){
                    return `<span class="badge bg-success">${data}</span> `
                }
            },
        ],
        language: {
            decimal:"",
            emptyTable:"No hay registros que mostrar en la tabla",
            info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
            infoEmpty:"Mostrando 0 de 0 de 0 registros",
            infoFiltered: "(filtrado de _MAX_ registros totales)",
            loadingRecords: "Cargando...",
            zeroRecords:    "No se encontraron registros",
            lengthMenu:     "Mostrar MENU registros",
            search: "",
            paginate: {
                first: "Primero",
                last: "Último",
                next: "Siguiente",
                previous: "Anterior"
            },
            infoFiltered:"(Filtrado de MAX total entradas)",
            infoPostFix:"",
            thousands:",",
            searchPlaceholder: "Buscar por documento",
            },
        deferRender: true,
        lengthChange: false,
    });

    
    $(".dataTables_length select").addClass('form-select');
    $('.dataTables_filter label').addClass('label-form');
    $('.dataTables_filter input').addClass('form-control rounded bg-light border-light');
    $('.dataTables_filter input').attr('placeholder', 'Buscar ...');

    // $('.dt-button').removeClass('dt-button');
    
    // Detectar cambios en los filtros y recargar tabla
    $('#filtroComida, #filtroCasino, #filtroFecha').on('change', function () {
        dataTable.ajax.reload();
    });
});
