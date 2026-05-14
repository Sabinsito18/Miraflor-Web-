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
    const submitButton = inscriptionForm.querySelector('button[type="submit"]');
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

    setFormStatus(status, 'Guardando inscripción...', 'info');
    if (submitButton) submitButton.disabled = true;

    fetch('/api/inscripciones', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then((response) => response.json().then((body) => ({ response, body })))
      .then(({ response, body }) => {
        if (!response.ok || !body.ok) {
          throw new Error(body.error || 'No se pudo guardar la inscripción.');
        }

        setFormStatus(status, 'Inscripción guardada correctamente. Nos pondremos en contacto contigo.', 'success');
        inscriptionForm.reset();
      })
      .catch((error) => {
        setFormStatus(
          status,
          `No se pudo guardar la inscripción. Abre la web desde http://127.0.0.1:8000 y revisa la conexión MySQL. Detalle: ${error.message}`,
          'error'
        );
      })
      .finally(() => {
        if (submitButton) submitButton.disabled = false;
      });
  });
});

function setFormStatus(status, message, type) {
  if (!status) return;

  status.textContent = message;
  status.dataset.type = type;
}
