let idRowClicked;
$(document).ready(function () {
    const url = $("#registroTable").data("url");
    dataTable = $("#registroTable").DataTable({
        responsive: {
            enabled: true,
            details: {
                type: "column", // permite expandir al hacer clic
                target: "tr", // clic en toda la fila
            },
        },
        processing: true,
        serverSide: true,
        dom: "Bfrtip",
        buttons: [
            {
                text: '<i class="fa-regular fa-file-excel"></i> Excel',
                className: "btn btn-success btn-sm",
                attr: {
                    title: "Exportar a Excel", // opcional
                },
                action: function () {
                    let params = $.param({
                        comida: $("#filtroComida").val(),
                        casino: $("#filtroCasino").val(),
                        fecha: $("#filtroFecha").val(),
                    });
                    window.location = "/export/excel/?" + params;
                },
                escapeHtml: false,
            },
            {
                text: '<i class="fa-regular fa-file-pdf"></i> PDF',
                className: "btn btn-danger btn-sm",
                action: function () {
                    let params = $.param({
                        comida: $("#filtroComida").val(),
                        casino: $("#filtroCasino").val(),
                        fecha: $("#filtroFecha").val(),
                    });
                    window.location = "/export/pdf/?" + params;
                },
                escapeHtml: false,
            },
        ],
        ajax: {
            url: url, // Ruta a tu vista de servidor
            data: function (d) {
                d.comida = $("#filtroComida").val();
                d.casino = $("#filtroCasino").val();
                d.fecha = $("#filtroFecha").val();
            },
            dataSrc: "data", // nombre del campo que contiene la lista de alarmas
        },
        columnDefs: [
            { responsivePriority: 1, targets: [3, 4, 5] }, // documento, casino, comida visibles en móvil
            { responsivePriority: 2, targets: [0, 1, 2] }, // los demás se ocultan primero
        ],
        columns: [
            {
                data: "fecha_hora",
                render: function (data, type, row) {
                    const date = new Date(data);
                    const options = {
                        year: "numeric",
                        month: "2-digit",
                        day: "2-digit",
                        hour: "2-digit",
                        minute: "2-digit",
                    };
                    return date
                        .toLocaleDateString("es-ES", options)
                        .replace(",", "");
                },
            },
            { data: "apellido" },
            { data: "nombre" },
            { data: "documento" },
            { data: "casino" },
            {
                data: "comida",
                render: function (data, type, row) {
                    const colores = {
                        desayuno: "bg-warning text-dark",
                        almuerzo: "bg-success",
                        merienda: "bg-primary",
                        cena: "bg-danger",
                    };

                    // si no existe en el mapa, usar color por defecto
                    const clase =
                        colores[data?.toLowerCase()] || "bg-secondary";

                    return `<span class="badge rounded-pill ${clase}">${data}</span>`;
                },
            },
        ],
        language: {
            decimal: "",
            emptyTable: "No hay registros que mostrar en la tabla",
            info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
            infoEmpty: "Mostrando 0 de 0 de 0 registros",
            infoFiltered: "(filtrado de _MAX_ registros totales)",
            loadingRecords: "Cargando...",
            zeroRecords: "No se encontraron registros",
            lengthMenu: "Mostrar MENU registros",
            search: "",
            paginate: {
                first: "|<<",
                last: ">>|",
                next: ">",
                previous: "<",
            },
            infoFiltered: "(Filtrado de MAX total entradas)",
            infoPostFix: "",
            thousands: ",",
            searchPlaceholder: "Buscar por DNI",
        },
        deferRender: true,
        lengthChange: false,
    });

    $('.dt-search').addClass('mt-2 mb-1');
    $('.dt-search input').addClass('rounded col-md-3 col-12 border-light');
    $(".dt-info").addClass("text-center");
    $(".dt-paging").addClass("d-flex justify-content-center");
    $(".dt-buttons").addClass("d-flex align-items-center justify-content-center gap-2");
    $(".dt-button").removeClass("dt-button");

    // Detectar cambios en los filtros y recargar tabla
    $("#filtroComida, #filtroCasino, #filtroFecha").on("change", function () {
        dataTable.ajax.reload();
    });
});
