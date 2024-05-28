$(document).ready(function() {
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

    // Función para mostrar el calendario cuando se selecciona una opción en Info_cita
    $('.Info_cita select').change(function() {
        const selectedOption = $(this).find('option:selected').text();
        $('#appointment-form input[name="titulo"]').val(selectedOption);
        $('.Info_cita').hide();
        $('.calendar-container').show();
            });

        for (let day = 1; day <= daysInMonth; day++) {
                $('#calendar').append('<div>' + day + '</div>');
            }

            let selectedDate = null;

    // Función para seleccionar un día en el calendario
    $('#calendar div').click(function() {
        selectedDate = $(this).text() + '/' + (currentMonth + 1) + '/' + currentYear;
        $('.calendar-container').hide();
        $('.interval-selection').show();
    });

    // Función para seleccionar un intervalo de tiempo
    $('#select-interval').click(function() {
        $('.interval-selection').hide();
        $('.hour-selection').show();

        const interval = parseInt($('#time-slot').val());
        const startHour = 7; // 7 AM
        const endHour = 17; // 5 PM
        const totalIntervals = 60 / interval;

        // Limpiar las horas anteriores
        $('.hour-column').empty();

        // Crear las celdas para los intervalos de cada hora
        for (let hour = startHour; hour < endHour; hour++) {
            for (let i = 0; i < totalIntervals; i++) {
                const minutes = i * interval;
                const formattedHour = hour.toString().padStart(2, '0') + ':' + minutes.toString().padStart(2, '0');
                $('.hour-column').eq(hour - startHour).append('<div data-hour="' + formattedHour + '">' + formattedHour + '</div>');
            }
        }
    });

    // Función para seleccionar una hora y mostrar el formulario
    $('.hour-column').on('click', 'div', function() {
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

    // Función para manejar el envío del formulario
    $('#appointment-form').submit(function(event) {
        event.preventDefault();
        alert('Cita registrada con éxito');
        // Aquí puedes agregar la lógica para enviar el formulario al servidor
    });
});
