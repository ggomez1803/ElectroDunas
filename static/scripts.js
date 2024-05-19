// Evento para manejar la subida de archivos
document.getElementById('uploadForm').addEventListener('submit', function(e) {
  e.preventDefault();
  var formData = new FormData(this);
  fetch('/upload', {
      method: 'POST',
      body: formData
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json();
  })
  .then(data => {
      alert(data.message);
  })
  .catch(error => {
      console.error('Upload error:', error);
      alert('Upload failed: ' + error.message);
  });
});

// Evento para manejar la ejecución del script de Python
document.getElementById('executeScript').addEventListener('click', function() {
  fetch('/execute-script', {
      method: 'GET'
  }).then(response => response.json())
    .then(data => {
      alert(data.message);
      console.log(data);
    })
    .catch(error => {
      alert('Error: ' + error);
      console.error('Error:', error);
    });
});

// Función para enviar la nueva ruta al servidor y actualizar config.json
function guardarConfig(configKey, inputId) {
  const newRuta = document.getElementById(inputId).value;
  fetch(`/update-config/${configKey}`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ new_path: newRuta })
  })
  .then(response => response.json())
  .then(data => {
      alert(data.message);
  })
  .catch(error => {
      console.error('Error al guardar la configuración:', error);
  });
}

// Función para alternar la visibilidad del menú lateral
function toggleSidebar() {
  var sidebar = document.getElementById('sidebar');
  var mainContent = document.querySelector('.main-content');
  sidebar.classList.toggle('minimized');
  mainContent.classList.toggle('expanded');
}

// Funciones para mostrar las secciones correspondientes
function showSection(sectionId) {
  // Oculta todas las secciones
  document.querySelectorAll('.content-section').forEach(section => {
      section.style.display = 'none';
  });
  // Muestra la sección solicitada
  document.getElementById(sectionId).style.display = 'block';
}

// Eventos para manejar los clics en las opciones del menú
document.getElementById('runCluster').addEventListener('click', function() {
  showSection('clusterSection');

});

document.getElementById('configuracion').addEventListener('click', function() {
   showSection('configSection');

 });

document.getElementById('about').addEventListener('click', function() {
  showSection('aboutSection');

  // Realiza una solicitud al servidor para obtener las rutas de configuración
  fetch('/get-config', {
      method: 'GET'
  })
  .then(response => response.json())
  .then(config => {
      // Actualiza el contenido de la sección About con las rutas de configuración
      document.getElementById('aboutContent').innerHTML = `
          <strong>Ruta Carpeta Consumos:</strong> ${config.ruta_carpeta_consumos}<br>
          <strong>Ruta Sector Clientes:</strong> ${config.ruta_sector_clientes}<br>
          <strong>Ruta Carpeta Exportación:</strong> ${config.ruta_carpeta_exportacion}
      `;
  })
  .catch(error => {
      console.error('Error al obtener la configuración:', error);
  });
});
