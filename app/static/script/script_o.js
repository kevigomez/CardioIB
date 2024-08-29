$(document).ready(function() {
    let blockedDates = [];
    const calendarContainer = document.getElementById('calendar');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    let selectedDate = new Date();
    let currentYear = selectedDate.getFullYear();
    let currentMonth = selectedDate.getMonth();



    function getMonthsArray(year, startMonth) {
        return Array.from({ length: 3 }, (_, i) => new Date(year, startMonth + i));
    }

    function renderCalendar(resourceId) {
        $('#schedule-table td').each(function() {
            let cellDate = $(this).data('date');
            let adjustedDate = new Date(cellDate);
            adjustedDate.setMinutes(adjustedDate.getMinutes() + adjustedDate.getTimezoneOffset()); // Ajuste para la zona horaria
            if (isDayBlocked(adjustedDate)) {
                $(this).addClass('blocked-day'); // Asegúrate de que esta clase tenga los estilos adecuados en CSS
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
                    }
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
        loadBlockedDates().then(() => {
            renderCalendar();
        });
    });

    nextBtn.addEventListener('click', () => {
        currentMonth += 3;
        if (currentMonth > 11) {
            currentMonth -= 12;
            currentYear += 1;
        }
        loadBlockedDates().then(() => {
            renderCalendar();
        });
    });
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
    
        // Redirigir inmediatamente
        let newUrl = `${citasUrl}?resource_id=${selectedResourceId}`;
        window.location.href = newUrl;
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
    // Renderiza el calendario primero
    renderCalendar(); 
    loadBlockedDates().then(() => {
        renderCalendar();
        loadAppointments();
    }).fail(function() {
        console.log('Error al cargar días bloqueados o citas');
    });
    let updateBaseUrl = updateCitasUrl;
    function loadBlockedDates() {
        let selectedResource = $('#cita-select').val();
        return $.ajax({
            url: blockedDatesUrl,
            method: "GET",
            data: { resource_id: selectedResource }, 
            success: function(response) {
                blockedDates = response.blocked_dates.map(date => {
                    // Crea una nueva fecha y ajusta para evitar desajustes por zona horaria
                    let localDate = new Date(date + "T00:00:00"); // Agrega la hora para que no se interprete como UTC
                    return localDate;
                });
                console.log("Días bloqueados cargados para el recurso:", selectedResource, blockedDates);
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

$(document).ready(function() {
    // Ocultar el menú contextual al hacer clic fuera de él
    $(document).click(function(e) {
        if (!$(e.target).closest('#contextMenu').length) {
            $('#contextMenu').hide();
        }
    });

    // Mostrar el menú contextual al hacer clic en una celda desocupada
    $('#schedule-table').on('click', '.empty-cell', function(e) {
        let cellDate = $(this).data('date');

        // Posicionar el menú contextual junto a la celda seleccionada
        $('#contextMenu').css({
            display: 'block',
            left: e.pageX,
            top: e.pageY
        });

        // Guardar la fecha seleccionada en los botones del menú
        $('#blockDayContextBtn').data('date', cellDate);
        $('#createAppointmentContextBtn').data('date', cellDate);
    });

    // Manejo del clic en "Bloquear día" en el menú contextual
    $('#blockDayContextBtn').click(function() {
        let selectedDate = $(this).data('date');
        bloquearDia(selectedDate);
        $('#contextMenu').hide(); // Ocultar el menú después de la acción
    });

    // Manejo del clic en "Crear cita" en el menú contextual
    $('#createAppointmentContextBtn').click(function() {
        let selectedDate = $(this).data('date');
        // Aquí puedes redirigir a la página de creación de citas o abrir un modal
        let createUrl = `${createAppointmentUrl}?date=${selectedDate}&resource_id=${$('#resource_id').val()}`;
        window.location.href = createUrl;
        $('#contextMenu').hide(); // Ocultar el menú después de la acción
    });

    // Función para bloquear el día (puedes modificarla según tu lógica)
    function bloquearDia(date) {
        $.ajax({
            url: blockDayUrl,  // Cambia este URL al correcto
            method: "POST",
            data: { date: date, resource_id: $('#resource_id').val() },
            success: function(response) {
                console.log('Día bloqueado:', date);
                // Refresca la tabla para mostrar los cambios
                loadBlockedDates($('#resource_id').val());
            },
            error: function(error) {
                console.log('Error al bloquear el día:', error);
            }
        });
    }
});

