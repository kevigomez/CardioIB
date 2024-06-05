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

    $('.Info_cita select').change(function() {
        const selectedOption = $(this).find('option:selected').text();
        $('#appointment-form input[name="titulo"]').val(selectedOption);
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
                $('.hour-column').eq(hour - startHour).append('   <div style="border-right: 1px solid #53577F;" display="none" data-hour="' + formattedHour + '">' + formattedHour + '</div>');
            }
        }
    });

    $('.hour-column').on('click', 'div', function() {
        const selectedHour = $(this).attr('data-hour');
        $('.hour-selection').hide();
        $('.form-container').show();

        const interval = parseInt($('#time-slot').val());

        if (selectedDate) {
            const selectedDateParts = selectedDate.split('/');
            const formattedDate = `${selectedDateParts[2]}-${selectedDateParts[1].padStart(2, '0')}-${selectedDateParts[0].padStart(2, '0')}`;

            const startTime = new Date(`${formattedDate}T${selectedHour}:00`);
            const endTime = new Date(startTime.getTime() + interval * 60000);

            $('#inicio-fecha').val(startTime.toISOString().slice(0, 10));
            $('#inicio-hora').val(startTime.toISOString().slice(11, 16));
            $('#fin-fecha').val(endTime.toISOString().slice(0, 10));
            $('#fin-hora').val(endTime.toISOString().slice(11, 16));
        } 
    });

    $('#appointment-form').submit(function(event) {
        event.preventDefault();
        alert('Cita registrada con éxito');
        // Aquí puedes agregar la lógica para enviar el formulario al servidor
    });
});
