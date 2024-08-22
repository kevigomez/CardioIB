$(document).ready(function() {
    let updateBaseUrl = updateCitasUrl;
    let blockedDates = [];

    function loadBlockedDates() {
        return $.ajax({
            url: blockedDatesUrl,
            method: "GET",
            success: function(response) {
                blockedDates = response.blocked_dates.map(date => {
                    let localDate = new Date(date);
                    localDate.setMinutes(localDate.getMinutes() + localDate.getTimezoneOffset());
                    return localDate;
                });
                console.log("Días bloqueados cargados:", blockedDates);
                renderCalendar();
            },
            error: function() {
                console.log('Error al cargar los días bloqueados');
            }
        });
    }

    function isDayBlocked(date) {
        return blockedDates.some(blockedDate => formatDate(date) === formatDate(blockedDate));
    }

    function loadAppointments() {
        let selectedResource = $('#cita-select').val();
        console.log("Recurso seleccionado:", selectedResource);

        $.ajax({
            url: appointmentsUrl,
            method: "GET",
            data: { resource_id: selectedResource },
            success: function(response) {
                let appointments = response.appointments;
                console.log("Respuesta del servidor:", response);

                appointments.forEach(appointment => {
                    let startDate = new Date(appointment.start);
                    let endDate = new Date(appointment.end);
                    let dateString = `${startDate.getFullYear()}-${String(startDate.getMonth() + 1).padStart(2, '0')}-${String(startDate.getDate()).padStart(2, '0')}`;
                    let timeSlot = `${String(startDate.getHours()).padStart(2, '0')}:${String(startDate.getMinutes()).padStart(2, '0')} - ${String(endDate.getHours()).padStart(2, '0')}:${String(endDate.getMinutes()).padStart(2, '0')}`;

                    console.log(`Buscando celda para fecha: ${dateString} y hora: ${timeSlot}`);

                    let cell = $(`#schedule-table td[data-date="${dateString}"][data-time="${timeSlot}"]`);

                    if (cell.length > 0) {
                        cell.addClass('has-appointment')
                            .attr('title', appointment.title)
                            .text(appointment.title)
                            .data('appointment-id', appointment.cita_id);
                        cell.off('click').removeClass('hour-column').addClass('has-appointment-cell');
                    }
                    else {
                        console.log(`No se encontró celda para la fecha: ${dateString} y hora: ${timeSlot}`);
                    }
                });

                $('.has-appointment').on('click', function() {
                    let appointmentId = $(this).data('appointment-id');
                    if (appointmentId) {
                        let updateUrl = updateBaseUrl.replace('0', appointmentId);
                        window.location.href = updateUrl;
                    } else {
                        console.log("Error: No se encontró el ID de la cita.");
                    }
                });
            },
            error: function(error) {
                console.log('Error al obtener las citas:', error);
            }
        });
    }
    function updateHourSelection(selectedDate) {
        if (isDayBlocked(selectedDate)) {
            console.log('Día seleccionado está bloqueado:', selectedDate);
            $('#schedule-table tbody').empty(); // Vaciar la tabla si el día está bloqueado
        } else {
            console.log('Día seleccionado no está bloqueado:', selectedDate);
            $.getJSON(timeIntervalUrl, function(data) {
                generateTable(selectedDate, parseInt(data.interval));
            });
        }
    }

    $.getJSON(timeIntervalUrl, function(data) {
        generateTable(selectedDate, parseInt(data.interval));
    });

    $('#paciente').on('input', function() {
        let query = $(this).val();
        if (query.length > 2) {
            $.ajax({
                url: searchUserUrl,
                method: "GET",
                data: { query: query},
                success: function(data) {
                    let results = data.results;
                    let tableBody = $('#resultsTable tbody');
                    tableBody.empty();

                    if (results.length > 0) {
                        $('#resultsTable').show();
                        results.forEach(function(user) {
                            let row = `<tr class="selectable">
                                <td>${user.fname} ${user.lname} (${user.organization})</td>
                            </tr>`;
                            tableBody.append(row);
                        });

                        $('.selectable').on('click', function() {
                            let selectedText = $(this).find('td').text();
                            $('#paciente').val(selectedText);
                            $('#resultsTable').hide();
                        });
                    } else {
                        $('#resultsTable').hide();
                    }
                },
                error: function(error) {
                    console.log('Error:', error);
                }
            });
        } else {
            $('#resultsTable').hide();
        }
    });

    $('#cita-select').change(function() {
        let selectedResourceId = $(this).val();
        $('#resource_id').val(selectedResourceId);
        loadAppointments();
        setTimeout(function() {
            let newUrl = `${citasUrl}?resource_id=${selectedResourceId}`;
            window.location.href = newUrl;
        }); // Ajusta el tiempo de espera según sea necesario
    });

    function generateTable(startDate, interval) {
        let start = "07:00";
        let end = "17:00";
        let slots = generateTimeSlots(start, end, interval);
    
        let tableHead = `<tr><th>Día y Fecha</th>${slots.map(slot => `<th>${slot}</th>`).join('')}</tr>`;
        let tableBody = '';
    
        let dayOfWeek = startDate.getDay();
        let monday = new Date(startDate);
        monday.setDate(startDate.getDate() - (dayOfWeek === 0 ? 6 : dayOfWeek - 1));
    
        for (let i = 0; i < 7; i++) {
            let currentDay = new Date(monday);
            currentDay.setDate(monday.getDate() + i);
            currentDay.setMinutes(currentDay.getMinutes() + currentDay.getTimezoneOffset()); // Ajuste para la zona horaria
    
            let dayOfWeekStr = currentDay.toLocaleString('es-ES', { weekday: 'long' });
            let date = currentDay.toLocaleDateString('es-ES');
    
            tableBody += `<tr><td>${dayOfWeekStr}, ${date}</td>${slots.map(slot => `<td class="hour-column" data-date="${formatDate(currentDay)}" data-time="${slot}"></td>`).join('')}</tr>`;
        }
    
        $('#schedule-table thead').html(tableHead);
        $('#schedule-table tbody').html(tableBody);
    
        $('.hour-column').off('click').on('click', function(){
            let dateString = $(this).data('date').split('T')[0];  
            let time = $(this).data('time');
            let [start, end] = time.split(' - ');
            console.log("Fecha seleccionada:", dateString);
        
            let duracion = calculateDuration(start, end);
            $('#duracion').text(duracion);
            $('#title').val(`Cita - ${$('.cita option:selected').text()}`);
            $('#inicio-fecha').val(dateString);
            $('#inicio-hora').val(formatTime(start));
            $('#fin-fecha').val(dateString);
            $('#fin-hora').val(formatTime(end));
        
            $('#title, #inicio-fecha, #fin-fecha').prop('readonly', true);
            $('.selecc').prop('readonly', true);
            $('.Info_cita').hide();
            $('.calendar-container').hide();
            $('.hour-selection').hide();
            $('.form-container').show();
        
            $('#resource_id').val($('#cita-select').val());
        }); 
        loadAppointments();
    }
    

    function formatDate(date) {
        let day = String(date.getDate()).padStart(2, '0');
        let month = String(date.getMonth() + 1).padStart(2, '0');
        let year = date.getFullYear();
        return `${year}-${month}-${day}`;
    }
    
    

    function formatTime(time) {
        let [hours, minutes] = time.split(':');
        return `${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}`;
    }

    function calculateDuration(start, end) {
        let startTime = new Date(`1970-01-01T${start}:00`);
        let endTime = new Date(`1970-01-01T${end}:00`);
        let duration = (endTime - startTime) / 60000; // duración en minutos
        let hours = Math.floor(duration / 60);
        let minutes = duration % 60;
        return `${hours} horas ${minutes} minutos`;
    }

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

    const calendarContainer = document.getElementById('calendar');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    let selectedDate = new Date();
    let currentYear = selectedDate.getFullYear();
    let currentMonth = selectedDate.getMonth();

    function updateCalendar() {
        let calendar = new FullCalendar.Calendar(calendarContainer, {
            initialView: 'dayGridMonth',
            locale: 'es',
            events: function(fetchInfo, successCallback, failureCallback) {
                let cita = $('#cita-select').val();

                $.ajax({
                    url: appointmentsUrl,
                    data: {
                        cita: cita,
                        start: fetchInfo.startStr,
                        end: fetchInfo.endStr
                    },
                    success: function(response) {
                        successCallback(response.appointments);
                    },
                    error: function() {
                        failureCallback('Error al cargar los eventos');
                    }
                });
            },
            eventClick: function(info) {
                let appointmentId = info.event.id;
                if (appointmentId) {
                    let updateUrl = updateBaseUrl.replace('0', appointmentId);
                    window.location.href = updateUrl;
                } else {
                    console.log("Error: No se encontró el ID de la cita.");
                }
            },
            headerToolbar: {
                start: '',
                center: 'title',
                end: ''
            },
            height: 'auto',
            datesSet: function() {
                $('.fc-day').each(function() {
                    let dateStr = $(this).data('date');
                    let date = new Date(dateStr);
                    if (isDayBlocked(date)) {
                        console.log(`Bloqueando día: ${dateStr}`);
                        $(this).addClass('fc-day-blocked');
                    } else {
                        $(this).removeClass('fc-day-blocked');
                    }
                });
            }
        });
        calendar.render();
    }

    function navigateCalendar(direction) {
        if (direction === 'prev') {
            currentMonth--;
        } else if (direction === 'next') {
            currentMonth++;
        }

        selectedDate = new Date(currentYear, currentMonth);
        updateCalendar();
    }

    function getMonthsArray(year, startMonth) {
        return Array.from({ length: 3 }, (_, i) => new Date(year, startMonth + i));
    }
    loadBlockedDates();
    function renderCalendar() {
        $('#schedule-table td').each(function() {
            let cellDate = $(this).data('date');
            let adjustedDate = new Date(cellDate);
            adjustedDate.setMinutes(adjustedDate.getMinutes() + adjustedDate.getTimezoneOffset()); // Ajuste para la zona horaria
            if (isDayBlocked(adjustedDate)) {
                $(this).addClass('blocked-day');
            }
        });
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
                let dayDate = new Date(date.getFullYear(), date.getMonth(), day);
                if (isDayBlocked(dayDate)) {
                    dayDiv.classList.add('blocked');
                }
                dayDiv.textContent = day;
                dayDiv.addEventListener('click', () => {
                    if (!dayDiv.classList.contains('blocked')) {
                        selectedDate = new Date(date.getFullYear(), date.getMonth(), day);
                        console.log('Fecha seleccionada:', selectedDate);
                        updateHourSelection(selectedDate);
                    }
                });
                daysDiv.appendChild(dayDiv);
            }

            monthDiv.appendChild(daysDiv);
            calendarContainer.appendChild(monthDiv);
        });

        if (!selectedDate) {
            const today = new Date();
            selectedDate = new Date(currentYear, currentMonth, today.getDate());
            updateHourSelection(selectedDate);
        } else {
            updateHourSelection(selectedDate);
        }
    }
    loadBlockedDates().then(() => {
        $.getJSON(timeIntervalUrl, function(data) {
            // Si la fecha seleccionada no está bloqueada, actualizar la tabla de horarios
            if (selectedDate && !isDayBlocked(selectedDate)) {
                generateTable(selectedDate, parseInt(data.interval));
            }
            loadAppointments();
        });
    });

    

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
});
$(document).ready(function() {
    $('.hour-column').datepicker({
        language: 'es',
        format: 'yyyy-mm-dd',
        beforeShowDay: function(date) {
            return !isDayBlocked(date);
        }
    });    
});


