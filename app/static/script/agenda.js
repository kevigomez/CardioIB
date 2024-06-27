$(document).ready(function() {
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        selectable: true,
        selectHelper: true,
        dayClick: function(date) {
            var selectedDate = date.format('YYYY-MM-DD');
            $('#selected-date').text('Citas para el día: ' + selectedDate);
            $('#schedule-container').show();
            loadSchedule(selectedDate);
        },
        events: [
            // Aquí puedes agregar eventos iniciales si lo deseas
        ]
    });
});

function loadSchedule(date) {
    $.get('/appointments/' + date, function(schedule) {
        var tbody = $('#schedule-table tbody');
        tbody.empty();
        
        for (var hour = 9; hour <= 17; hour++) {
            var timeSlot = hour + ':00 - ' + (hour + 1) + ':00';
            var appointment = schedule[timeSlot] || '';
            
            var row = $('<tr>');
            row.append('<td>' + timeSlot + '</td>');
            row.append('<td>' + appointment + '</td>');
            row.click(function() {
                var time = $(this).children('td:first').text();
                var appointment = prompt('Agendar cita para ' + date + ' a las ' + time + ':');
                if (appointment) {
                    saveAppointment(date, time, appointment);
                }
            });
            tbody.append(row);
        }
    });
}

function saveAppointment(date, time, appointment) {
    $.post('/appointments', { date: date, time: time, appointment: appointment }, function(response) {
        if (response.success) {
            loadSchedule(date);
        } else {
            alert('Error al guardar la cita');
        }
    });
}
