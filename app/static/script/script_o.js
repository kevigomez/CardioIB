$(document).ready(function() {
    // Función para generar intervalos de tiempo
    function generateTimeSlots(start, end, interval) {
        let slots = [];
        let startTime = new Date();
        startTime.setHours(start.split(':')[0], start.split(':')[1], 0, 0);
        let endTime = new Date();
        endTime.setHours(end.split(':')[0], end.split(':')[1], 0, 0);

        while (startTime < endTime) {
            let endTimeSlot = new Date(startTime.getTime() + interval * 60000);
            slots.push(`${startTime.getHours().toString().padStart(2, '0')}:${startTime.getMinutes().toString().padStart(2, '0')} - ${endTimeSlot.getHours().toString().padStart(2, '0')}:${endTimeSlot.getMinutes().toString().padStart(2, '0')}`);
            startTime = endTimeSlot;
        }
        return slots;
    }

    // Función para generar la tabla de horarios
    function generateTable(interval) {
        let start = "07:00";
        let end = "17:00";
        let slots = generateTimeSlots(start, end, interval);
        let days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"];

        let tableHead = `<tr><th>Día</th>${slots.map(slot => `<th>${slot}</th>`).join('')}</tr>`;
        let tableBody = days.map(day => `<tr><td>${day}</td>${slots.map(slot => `<td class="hour-column"></td>`).join('')}</tr>`).join('');

        $('#schedule-table thead').html(tableHead);
        $('#schedule-table tbody').html(tableBody);
    }

    // Obtener el intervalo de tiempo desde el servidor y generar la tabla
    $.getJSON("{{ url_for('main.get_time_interval') }}", function(data) {
        generateTable(parseInt(data.interval));

        // Adjuntar el evento de clic a las celdas de la columna de horas
        $('.hour-column').on('click', function() {
            $('.form-container').show();
        });
    });

    // Código para el calendario
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
                    selectedDate = `${day}/${date.getMonth() + 1}/${date.getFullYear()}`;
                    $('.calendar-container').hide();
                    $('.interval-selection').show();
                });
                daysDiv.appendChild(dayDiv);
            }

            monthDiv.appendChild(daysDiv);
            calendarContainer.appendChild(monthDiv);
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

    $('#appointment-form').submit(function(event) {
        event.preventDefault();
        alert('Cita registrada con éxito');
        // Aquí puedes agregar la lógica para enviar el formulario al servidor
    });
});
