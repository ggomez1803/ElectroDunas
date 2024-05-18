// scripts.js
document.getElementById('uploadForm').addEventListener('submit', function(e) {
  e.preventDefault(); // Evita que el formulario se envíe de la manera tradicional
  var formData = new FormData(this); // Crea un FormData con los archivos seleccionados
  fetch('/upload', { // Envía la solicitud al endpoint /upload
      method: 'POST',
      body: formData
  }).then(response => response.json())
    .then(data => {
      alert(data.message); // Muestra un mensaje con la respuesta del servidor
      console.log(data);
    })
    .catch(error => {
      alert('Error: ' + error); // Muestra un mensaje si hay un error
      console.error('Error:', error);
    });
});

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
