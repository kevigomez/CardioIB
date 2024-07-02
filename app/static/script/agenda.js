$(document).ready(function() {
    const calendarContainer = document.getElementById('calendar');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    let selectedDate;
    let currentYear = new Date().getFullYear();
    let currentMonth = new Date().getMonth();

    function getMonthsArray(year, startMonth) {
        return Array.from({ length: 3 }, (_, i) => new Date(year, startMonth + i));
    }

    function renderCalendar() {
        calendarContainer.innerHTML = '';
        const months = getMonthsArray(currentYear, currentMonth);
        months.forEach(date => {
            const monthDiv = document.createElement('div');
            monthDiv.className = 'month';

            const monthNameDiv = document.createElement('div');
            monthNameDiv.className = 'month-name';
            monthNameDiv.textContent = date.toLocaleString('es-ES', { month: 'long', year: 'numeric' });
            monthDiv.appendChild(monthNameDiv);

            const weekdaysDiv = document.createElement('div');
            weekdaysDiv.className = 'weekdays';
            ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'].forEach(day => {
                const weekdayDiv = document.createElement('div');
                weekdayDiv.className = 'weekday';
                weekdayDiv.textContent = day;
                weekdaysDiv.appendChild(weekdayDiv);
            });
            monthDiv.appendChild(weekdaysDiv);

            const daysDiv = document.createElement('div');
            daysDiv.className = 'days';
            const firstDay = new Date(date.getFullYear(), date.getMonth(), 1).getDay() || 7;
            const daysInMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();

            for (let i = 1; i < firstDay; i++) {
                const emptyDiv = document.createElement('div');
                emptyDiv.className = 'day empty';
                daysDiv.appendChild(emptyDiv);
            }

            for (let day = 1; day <= daysInMonth; day++) {
                const dayDiv = document.createElement('div');
                dayDiv.className = 'day';
                dayDiv.textContent = day;
                dayDiv.addEventListener('click', () => {
                    selectedDate = new Date(date.getFullYear(), date.getMonth(), day);
                    renderDayTable(selectedDate);
                    $('.calendar-container').hide();
                    $('.interval-selection').show();
                });
                daysDiv.appendChild(dayDiv);
            }

            monthDiv.appendChild(daysDiv);
            calendarContainer.appendChild(monthDiv);
        });
    }

    function renderDayTable(selectedDate) {
        const daysTableContainer = document.querySelector('.days-table-container');
        daysTableContainer.innerHTML = ''; // Clear previous content

        const table = document.createElement('table');
        table.className = 'days-table';

        const headerRow = document.createElement('tr');
        for (let i = 0; i < 4; i++) {
            const th = document.createElement('th');
            const date = new Date(selectedDate);
            date.setDate(selectedDate.getDate() + i);
            th.textContent = date.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'short' });
            headerRow.appendChild(th);
        }
        table.appendChild(headerRow);

        for (let hour = 7; hour < 18; hour++) {
            const row = document.createElement('tr');
            for (let i = 0; i < 4; i++) {
                const cell = document.createElement('td');
                const date = new Date(selectedDate);
                date.setDate(selectedDate.getDate() + i);
                cell.textContent = `${hour.toString().padStart(2, '0')}:00`;
                cell.dataset.date = date.toISOString().split('T')[0];
                cell.dataset.hour = hour;
                cell.className = 'time-slot';
                row.appendChild(cell);
            }
            table.appendChild(row);
        }

        daysTableContainer.appendChild(table);

        // Add event listener for time slots
        document.querySelectorAll('.time-slot').forEach(slot => {
            slot.addEventListener('click', () => {
                const date = slot.dataset.date;
                const hour = slot.dataset.hour;
                $('#inicio-fecha').val(date);
                $('#inicio-hora').val(`${hour.toString().padStart(2, '0')}:00`);
                $('#fin-fecha').val(date);
                $('#fin-hora').val(`${(parseInt(hour) + 1).toString().padStart(2, '0')}:00`);
                $('.interval-selection').hide();
                $('.form-container').show();
            });
        });
    }

    prevBtn.addEventListener('click', () => {
        currentMonth -= 3;
        if (currentMonth < 0) {
            currentMonth += 12;
            currentYear -= 1;
        }
        renderCalendar();
    });

    nextBtn.addEventListener('click', () => {
        currentMonth += 3;
        if (currentMonth > 11) {
            currentMonth -= 12;
            currentYear += 1;
        }
        renderCalendar();
    });

    renderCalendar();

    $('.Info_cita select').change(function() {
        const selectedOption = $(this).find('option:selected').text();
        $('#appointment-form input[name="title"]').val(selectedOption);
        $('.Info_cita').hide();
        $('.calendar-container').show();
    });

    $('#select-interval').click(function() {
        $('.interval-selection').hide();
        $('.hour-selection').show();

        const interval = parseInt($('#time-slot').val());
        const startHour = 7;
        const endHour = 17;
        const totalIntervals = 60 / interval;

        $('.hour-column').empty();

        for (let hour = startHour; hour < endHour; hour++) {
            for (let i = 0; i < totalIntervals; i++) {
                const minutes = i * interval;
                const formattedHour = hour.toString().padStart(2, '0') + ':' + minutes.toString().padStart(2, '0');
                $('.hour-column').eq(hour - startHour).append(`<div style="border-right: 1px solid #53577F;" display="none" data-hour="${formattedHour}">${formattedHour}</div>`);
            }
        }
    });

    $('#appointment-form').submit(function(event) {
        event.preventDefault();
        const appointment = {
            title: $('#title').val(),
            description: $('#description').val(),
            startDate: $('#inicio-fecha').val(),
            startTime: $('#inicio-hora').val(),
            endDate: $('#fin-fecha').val(),
            endTime: $('#fin-hora').val(),
            repeat: $('select[name="repetir"]').val(),
            resources: $('select[name="recursos"]').val(),
            patient: $('input[name="paciente"]').val(),
            age: $('input[name="edad"]').val(),
            status: $('select[name="estado"]').val(),
            authorization: $('input[name="autorizacion"]').val(),
            priority: $('select[name="prioridad"]').val(),
            callRecord: $('select[name="registro_llamada"]').val(),
            which: $('input[name="cual"]').val(),
        };

        saveAppointment(appointment);
        alert('Cita registrada con éxito');
        location.reload();
    });

    function saveAppointment(appointment) {
        let appointments = JSON.parse(localStorage.getItem('appointments')) || [];
        appointments.push(appointment);
        localStorage.setItem('appointments', JSON.stringify(appointments));
    }
});
