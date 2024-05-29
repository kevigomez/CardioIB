const calendarContainer = document.getElementById('calendar');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');

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
