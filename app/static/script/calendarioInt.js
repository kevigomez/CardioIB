
    $(document).ready(function() {
        $('#calendar').fullCalendar({
            selectable: true,
            select: function(start, end) {
                let selectedDate = start.format('YYYY-MM-DD');
                $('#selected-date').text(selectedDate);
                fetchAppointments(selectedDate);
            }
        });
    });

    function fetchAppointments(date) {
        $.ajax({
            url: '/get_appointments',
            data: { date: date },
            success: function(data) {
                let appointmentsList = $('#appointments-list');
                appointmentsList.empty();
                data.forEach(function(appointment) {
                    appointmentsList.append(`<tr><td>${appointment.time}</td><td>${appointment.description}</td></tr>`);
                });
                $('#appointments').show();
            }
        });
    }

    function addAppointment() {
        let date = $('#selected-date').text();
        let time = prompt('Enter time (HH:MM):');
        let description = prompt('Enter description:');
        let userId = 1;  // Assume user ID is 1 for this example

        $.ajax({
            url: '/add_appointment',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                date: date,
                time: time,
                description: description,
                user_id: userId
            }),
            success: function() {
                fetchAppointments(date);
            }
        });
    }