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

    function renderCalendar(scheduleId, weekDay) {
        // Limpiar el contenido del contenedor del calendario
        calendarContainer.innerHTML = '';
    
        // Llamar al backend para obtener los intervalos del día
        fetch(`/get_intervalos/${scheduleId}?weekDay=${weekDay}`)
            .then(response => response.json())
            .then(data => {
                const { intervals, dayStart, dayEnd } = data; // Destructuring para obtener intervalos y los límites del día
                const months = getMonthsArray(currentYear, currentMonth); // Obtener los meses para renderizar
                const hourStart = parseInt(dayStart.split(':')[0]);
                const hourEnd = parseInt(dayEnd.split(':')[0]);
    
                // Iterar sobre cada mes del año
                months.forEach(date => {
                    const monthDiv = document.createElement('div');
                    monthDiv.className = 'month';
    
                    // Renderizar el nombre del mes
                    const monthNameDiv = document.createElement('div');
                    monthNameDiv.className = 'month-name';
                    monthNameDiv.textContent = date.toLocaleString('es-ES', { month: 'long', year: 'numeric' });
                    monthDiv.appendChild(monthNameDiv);
    
                    // Renderizar los días de la semana
                    const weekdaysDiv = document.createElement('div');
                    weekdaysDiv.className = 'weekdays';
                    ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'].forEach(day => {
                        const weekdayDiv = document.createElement('div');
                        weekdayDiv.className = 'weekday';
                        weekdayDiv.textContent = day;
                        weekdaysDiv.appendChild(weekdayDiv);
                    });
                    monthDiv.appendChild(weekdaysDiv);
    
                    // Renderizar los días del mes
                    const daysDiv = document.createElement('div');
                    daysDiv.className = 'days';
                    const firstDay = new Date(date.getFullYear(), date.getMonth(), 1).getDay() || 7;
                    const daysInMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
    
                    // Rellenar los días vacíos antes del primer día del mes
                    for (let i = 1; i < firstDay; i++) {
                        const emptyDiv = document.createElement('div');
                        emptyDiv.className = 'day empty';
                        daysDiv.appendChild(emptyDiv);
                    }
    
                    // Renderizar los días del mes con base en los intervalos citables
                    for (let day = 1; day <= daysInMonth; day++) {
                        const dayDiv = document.createElement('div');
                        dayDiv.className = 'day';
                        let dayDate = new Date(date.getFullYear(), date.getMonth(), day);
                        
                        // Verificar si hay intervalos citables disponibles para ese día
                        const availableIntervals = intervals.filter(interval => {
                            const hourStartInterval = parseInt(interval.intervalStart.split(':')[0]);
                            const hourEndInterval = parseInt(interval.intervalEnd.split(':')[0]);
                            return hourStartInterval >= hourStart && hourEndInterval <= hourEnd;
                        });
    
                        // Si hay intervalos disponibles, mostramos el día como disponible
                        if (availableIntervals.length > 0) {
                            dayDiv.classList.add('citable');
                            dayDiv.textContent = day;
                            dayDiv.addEventListener('click', () => {
                                selectedDate = new Date(date.getFullYear(), date.getMonth(), day);
                                console.log('Fecha seleccionada:', selectedDate);
                            });
                        } else {
                            dayDiv.classList.add('blocked');
                        }
                        
    
                        daysDiv.appendChild(dayDiv);
                    }
    
                    monthDiv.appendChild(daysDiv);
                    calendarContainer.appendChild(monthDiv);
                });
            })
            .catch(error => console.error('Error al obtener los intervalos:', error));
    }
    
    // Llamar a renderCalendar para el horario y día seleccionados
    renderCalendar(scheduleId, 'lunes'); // Por ejemplo, para lunes
    
    

    prevBtn.addEventListener('click', () => {
        currentMonth -= 3;
        if (currentMonth < 0) {
            currentMonth += 12;
            currentYear -= 1;
        }
        loadBlockedDates().then(() => {
            renderCalendar(scheduleId, weekDay); // Pasar los parámetros correctos
        });
    });
    
    nextBtn.addEventListener('click', () => {
        currentMonth += 3;
        if (currentMonth > 11) {
            currentMonth -= 12;
            currentYear += 1;
        }
        loadBlockedDates().then(() => {
            renderCalendar(scheduleId, weekDay); // Pasar los parámetros correctos
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
        return $.ajax({
            url: timeIntervalUrl.replace('0', selectedResourceId),  // Inserta el schedule_id en la URL
            method: "GET",
            data: { 
                weekDay: dayOfWeek  // Envía el dayOfWeek en los parámetros
            },
            success: function(response) {
                let intervals = response.intervals;
    
                // Filtrar los intervalos según el tipo
                let citables = intervals.filter(interval => interval.tipe === 'citable');
                let bloqueosManuales = intervals.filter(interval => interval.tipe === 'bloqueado');
    
                console.log("Intervalos citables:", citables);
                console.log("Bloqueos manuales:", bloqueosManuales);
    
                // Generar las celdas solo con los intervalos citables y bloqueos
                generateTimeSlots(citables, bloqueosManuales);
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
    loadBlockedDates().then(() => {
        renderCalendar(scheduleId, weekDay);
        loadAppointments();  // Esto debería actualizar las citas en el calendario
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


