const usuarios = []; // Aquí se cargarían los datos de los usuarios
let currentPage = 1; // Variable global para almacenar el número de página actual


// Manejador de eventos para el botón "Siguiente"
document.getElementById('next-btn').addEventListener('click', () => {
    const maxPage = Math.ceil(usuarios.length / pageSize); // Calcula el número máximo de páginas
    currentPage++; // Incrementa el número de página
    if (currentPage > maxPage) {
        currentPage = maxPage; // Asegura que el número de página no sea mayor que el máximo
    }
    mostrarUsuarios(currentPage, pageSize); // Vuelve a mostrar los usuarios con la página actualizada
});
const pageSize = 10; // Cantidad de usuarios por página
mostrarUsuarios(1, pageSize);
