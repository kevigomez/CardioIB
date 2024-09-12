$(document).ready(function() {
    $('#week-day-select').change(function() {
        let selectedWeekDay = $(this).val();  // Obtiene el valor del select
        console.log("Día de la semana seleccionado:", selectedWeekDay);
        // Actualiza la URL para los intervalos
        timeIntervalUrl = updateTimeIntervalUrl(scheduleId, selectedWeekDay);
        loadTimeIntervals();  // Llama a la función para cargar los intervalos
    });
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

    function loadTimeIntervals() {
        let selectedResourceId = $('#cita-select').val();  // Aquí seleccionas el schedule_id desde el campo
        let selectedDate = $('#schedule-table').data('selected-date');
        let dayOfWeek = new Date(selectedDate).getDay();  // Obtiene el día de la semana (0-6)
    
        // Solicita los intervalos al servidor
        $.ajax({
            url: timeIntervalUrl.replace('0', selectedResourceId),  // Inserta el schedule_id en la URL
            method: "GET",
            data: { 
                weekDay: dayOfWeek  // Envía el dayOfWeek en los parámetros
            },
            success: function(response) {
                // Verifica que la respuesta tenga la propiedad 'intervals'
                if (response && response.intervals) {
                    let intervals = response.intervals;
    
                    // Filtrar los intervalos según el tipo
                    let citables = intervals.filter(interval => interval.tipe === 'citable');
                    let bloqueosManuales = intervals.filter(interval => interval.tipe === 'bloqueado');
    
                    console.log("Intervalos citables:", citables);
                    console.log("Bloqueos manuales:", bloqueosManuales);
    
                    // Generar las celdas solo con los intervalos citables y bloqueos
                    generateTimeSlots(citables, bloqueosManuales);
                } else {
                    console.log("La respuesta no contiene 'intervals'. Respuesta recibida:", response);
                }
            },
            error: function(error) {
                console.log("Error al obtener los intervalos:", error);
            }
        });
    }
    
    
    
    

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
    
    

    function generateTableForWeek(scheduleId) {
        let weekDays = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'];
    
        for (let i = 0; i < 7; i++) {
            let weekDay = weekDays[i];
            
            $.ajax({
                url: `/get_intervalos/${scheduleId}?weekDay=${weekDay}`,
                method: 'GET',
                success: function(data) {
                    // data contiene los intervalos citables para el día y el schedule
                    if (data.intervals && data.intervals.length > 0) {
                        let startTime = data.blockStart; // Inicio del día (bloqueo)
                        let endTime = data.blockEnd;     // Fin del día (bloqueo)
                        let citables = data.intervals;   // Intervalos citables
    
                        // Generar la tabla para cada día de la semana
                        let dayTable = `<tr><th>${capitalizeFirstLetter(weekDay)}</th>`;
    
                        // Recorrer cada intervalo citable y agregarlo a la tabla
                        for (let interval of citables) {
                            dayTable += `<td class="citable hour-column" data-start="${interval.start}" data-end="${interval.end}" data-weekday="${weekDay}">${interval.start} - ${interval.end}</td>`;
                        }
    
                        dayTable += '</tr>';
                        $('#schedule-table tbody').append(dayTable);
                    }
                }
            });
        }
    }
    
    // Esta función capitaliza la primera letra del día
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
    
    // Llamada inicial para generar la tabla de la semana basándose en el scheduleId
    let scheduleId = 1; // Reemplaza con el id correcto
    generateTableForWeek(scheduleId);
    
    // Evento click en las celdas citables
    $(document).on('click', '.hour-column.citable', function() {
        let startTime = $(this).data('start');
        let endTime = $(this).data('end');
        let weekDay = $(this).data('weekday');
        let day = $(this).closest('tr').find('th').text();
    
        let dateString = new Date().toISOString().split('T')[0];  // Ajustar para que coincida con el día seleccionado
        let duracion = calculateDuration(startTime, endTime);
        
        console.log(`Cita seleccionada el ${day} de ${startTime} a ${endTime}`);
        
        // Mostrar el formulario con los detalles de la cita seleccionada
        $('#duracion').text(duracion);
        $('#title').val(`Cita - ${$('.cita option:selected').text()}`);
        $('#inicio-fecha').val(dateString);
        $('#inicio-hora').val(formatTime(startTime));
        $('#fin-fecha').val(dateString);
        $('#fin-hora').val(formatTime(endTime));
    
        $('#title, #inicio-fecha, #fin-fecha').prop('readonly', true);
        $('.selecc').prop('readonly', true);
        $('.Info_cita').hide();
        $('.calendar-container').hide();
        $('.hour-selection').hide();
        $('.form-container').show();
    
        $('#resource_id').val($('#cita-select').val());
    });
    
    // Función para cargar citas ya existentes (debes implementarla)
    function loadAppointments() {
        // Aquí puedes agregar la lógica para cargar citas ya creadas
        // y marcarlas como ocupadas o mostrarlas en el calendario
    }
    
    
    
    function generateTimeSlots(start, end, interval) {
        let slots = [];
        let currentTime = start;
        
        while (currentTime < end) {
            let nextTime = addMinutes(currentTime, interval);
            slots.push(`${currentTime} - ${nextTime}`);
            currentTime = nextTime;
        }
        
        return slots;
    }
    
    function addMinutes(time, minsToAdd) {
        let [hours, minutes] = time.split(':').map(Number);
        minutes += minsToAdd;
        if (minutes >= 60) {
            hours += Math.floor(minutes / 60);
            minutes = minutes % 60;
        }
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
    }
    
    function formatDate(date) {
        const d = new Date(date);
        if (isNaN(d.getTime())) {
            console.error("Fecha inválida:", date);
            return "Invalid Date";
        }
        return d.toLocaleDateString(); // Cambia el formato si es necesario
    }
    
    
    
    function formatTime(time) {
        return time.padStart(5, '0');
    }
    
    function calculateDuration(start, end) {
        let [startHours, startMinutes] = start.split(':').map(Number);
        let [endHours, endMinutes] = end.split(':').map(Number);
        
        let startDate = new Date(0, 0, 0, startHours, startMinutes);
        let endDate = new Date(0, 0, 0, endHours, endMinutes);
        
        let diff = (endDate - startDate) / 1000 / 60;
        let hours = Math.floor(diff / 60);
        let minutes = diff % 60;
        
        return `${hours}h ${minutes}min`;
    }
    
    function loadAppointments() {
        // Aquí puedes cargar las citas existentes y mostrarlas en la tabla
    }
    

    function generateTimeSlots(citables, bloqueosManuales) {
        let tableBody = '';
        let currentDay = $('#schedule-table').data('selected-date');
    
        // Iterar sobre los intervalos citables y generar las celdas correspondientes
        citables.forEach(interval => {
            let startTime = interval.intervalStart;
            let endTime = interval.intervalEnd;
            let isBlocked = bloqueosManuales.some(bloqueo => bloqueo.intervalStart === startTime && bloqueo.intervalEnd === endTime);
    
            // Si el intervalo está bloqueado manualmente, lo marcamos como no disponible
            if (isBlocked) {
                tableBody += `<tr><td>${formatTime(startTime)} - ${formatTime(endTime)}</td>`;
                tableBody += `<td class="hour-column blocked" data-date="${formatDate(currentDay)}" data-time="${startTime} - ${endTime}">Bloqueado</td>`;
            } else {
                tableBody += `<tr><td>${formatTime(startTime)} - ${formatTime(endTime)}</td>`;
                tableBody += `<td class="hour-column available" data-date="${formatDate(currentDay)}" data-time="${startTime} - ${endTime}"></td>`;
            }
            tableBody += `</tr>`;
        });
    
        $('#schedule-table tbody').html(tableBody);
    
        // Añade eventos de clic a los intervalos disponibles
        $('.hour-column.available').off('click').on('click', function() {
            let timeSlot = $(this).data('time');
            let date = $(this).data('date');
            console.log("Fecha seleccionada:", date, "Intervalo:", timeSlot);
    
            // Actualiza los campos del formulario según el intervalo seleccionado
            $('#inicio-hora').val(timeSlot.split(' - ')[0]);
            $('#fin-hora').val(timeSlot.split(' - ')[1]);
            $('#inicio-fecha').val(date);
            $('#fin-fecha').val(date);
        });
    
        // Estilo para los intervalos bloqueados manualmente
        $('.hour-column.blocked').css({
            'background-color': '#FF0000',  // Rojo para los bloqueados
            'color': '#FFFFFF',             // Texto blanco para contraste
            'pointer-events': 'none'        // Deshabilitar clics en intervalos bloqueados
        });
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