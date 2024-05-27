$(document).ready(function() {
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

    for (let day = 1; day <= daysInMonth; day++) {
        $('#calendar').append('<div>' + day + '</div>');
    }

    let selectedDate = null;

    $('#calendar div').click(function() {
        selectedDate = $(this).text() + '/' + (currentMonth + 1) + '/' + currentYear;
        $('.calendar-container').hide();
        $('.interval-selection').show();
    });

    $('#select-interval').click(function() {
        $('.interval-selection').hide();
        $('.hour-selection').show();

        const interval = parseInt($('#time-slot').val());
        const startHour = 7; // 7 AM
        const endHour = 17; // 5 PM
        const totalIntervals = 60 / interval;

        $('#hours').empty(); // Limpiar las horas anteriores

        // Crear las filas de la tabla
        for (let hour = startHour; hour < endHour; hour++) {
            const row = $('<tr></tr>');

            // Añadir una celda para cada hora
            for (let i = 0; i < totalIntervals; i++) {
                const minutes = i * interval;
                const formattedHour = hour.toString().padStart(2, '0') + ':' + minutes.toString().padStart(2, '0');
                row.append('<td data-hour="' + formattedHour + '">' + formattedHour + '</td>');
            }

            // Añadir la fila a la tabla
            $('#hours').append(row);
        }
    });

    $('#hours').on('click', 'td', function() {
        const selectedHour = $(this).attr('data-hour');
        $('.hour-selection').hide();
        $('.form-container').show();

        const interval = parseInt($('#time-slot').val());
        const selectedDateParts = selectedDate.split('/');
        const formattedDate = `${selectedDateParts[2]}-${selectedDateParts[1].padStart(2, '0')}-${selectedDateParts[0].padStart(2, '0')}`;

        const startTime = new Date(`${formattedDate}T${selectedHour}:00`);
        const endTime = new Date(startTime.getTime() + interval * 60000);

        $('#inicio-fecha').val(startTime.toISOString().slice(0, 10));
        $('#inicio-hora').val(startTime.toISOString().slice(11, 16));
        $('#fin-fecha').val(endTime.toISOString().slice(0, 10));
        $('#fin-hora').val(endTime.toISOString().slice(11, 16));
    });

    $('#appointment-form').submit(function(event) {
        event.preventDefault();
        alert('Cita registrada con éxito');
        // Aquí puedes agregar la lógica para enviar el formulario al servidor
    });
});
