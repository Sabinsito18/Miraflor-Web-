// ======================
// MENU HAMBURGUESA
// ======================
const menuToggle = document.getElementById('menuToggle');
const navMenu = document.getElementById('navMenu');

if (menuToggle && navMenu) {
  menuToggle.addEventListener('click', () => {
    navMenu.classList.toggle('nav--open');

    const isOpen = navMenu.classList.contains('nav--open');
    menuToggle.textContent = isOpen ? '✕' : '☰';
    menuToggle.setAttribute('aria-expanded', String(isOpen));
  });
}

// ======================
// FORMULARIO INSCRIPCION
// ======================
document.addEventListener('DOMContentLoaded', () => {
  const inscriptionForm = document.querySelector('.inscription-form');

  if (!inscriptionForm) return;

  inscriptionForm.addEventListener('submit', (event) => {
    event.preventDefault();

    if (!inscriptionForm.reportValidity()) return;

    const data = new FormData(inscriptionForm);
    const status = document.getElementById('formStatus');
    const payload = {
      nombre_alumno: data.get('nombre'),
      apellidos_alumno: data.get('apellidos'),
      fecha_nacimiento: data.get('fecha-nac'),
      categoria: data.get('categoria'),
      experiencia: data.get('experiencia') || '',
      tutor: data.get('tutor'),
      telefono: data.get('tel'),
      email: data.get('email'),
      observaciones: data.get('obs') || '',
      privacidad: data.get('privacidad') === 'on'
    };

    if (status) {
      status.textContent = 'Guardando inscripción...';
    }

    fetch('/api/inscripciones', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then((response) => {
        if (!response.ok) throw new Error('No se pudo guardar la inscripción');
        return response.json();
      })
      .then(() => {
        if (status) {
          status.textContent = 'Inscripción guardada correctamente. Nos pondremos en contacto contigo.';
        }
        inscriptionForm.reset();
      })
      .catch(() => {
        sendInscriptionByEmail(payload, status);
      });
  });
});

function sendInscriptionByEmail(payload, status) {
  const subject = 'Inscripción A.C.D. Miraflor';
  const body = [
    'Datos del alumno',
    `Nombre: ${payload.nombre_alumno} ${payload.apellidos_alumno}`,
    `Fecha de nacimiento: ${payload.fecha_nacimiento}`,
    `Categoría: ${payload.categoria}`,
    `Experiencia previa: ${payload.experiencia || 'No indicada'}`,
    '',
    'Datos del tutor',
    `Tutor: ${payload.tutor}`,
    `Teléfono: ${payload.telefono}`,
    `Email: ${payload.email}`,
    '',
    'Información adicional',
    payload.observaciones || 'Sin observaciones'
  ].join('\n');

  if (status) {
    status.textContent = 'No se encontró el servidor. Se abrirá tu aplicación de correo para completar el envío.';
  }

  window.location.href = `mailto:info@acdmiraflor.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}
