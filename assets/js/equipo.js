/* =====================
    ELEMENTOS DEL DOM
===================== */
const teamGrid = document.getElementById('teamGrid');
const modal = document.getElementById('playerModal');
const closeModalBtn = document.getElementById('closeModal');

const modalImg = document.getElementById('modalImg');
const modalName = document.getElementById('modalName');
const modalPosition = document.querySelector('.modal__position');
const modalNumber = document.getElementById('modalNumber');
const modalAge = document.getElementById('modalAge');
const modalHeight = document.getElementById('modalHeight');
const modalDescription = document.getElementById('modalDescription');

let players = [];

function ready(el) {
  return el !== null && el !== undefined;
}


/* =====================
    CARGA DE DATOS
===================== */
// Si la web corre con server.py, usamos la base de datos. Si se abre como HTML, usamos el JSON.
fetch('/api/jugadores')
  .then(res => {
    if (!res.ok) throw new Error('API no disponible');
    return res.json();
  })
  .catch(() => fetch('../data/jugadores.json').then(res => {
    if (!res.ok) throw new Error('No se encontró el JSON');
    return res.json();
  }))
  .then(data => {
    players = data;
    renderTeam();
  })
  .catch(err => {
    console.error('Error cargando jugadores:', err);
    if (teamGrid) teamGrid.innerHTML = '<p>Error al cargar la plantilla.</p>';
  });

/* =====================
    RENDERIZADO
===================== */
function renderTeam() {
  if (!teamGrid) return;

  teamGrid.innerHTML = players.map(player => `
    <article class="player-card" data-id="${player.id}" tabindex="0">
      <img src="../${player.foto}" alt="${player.nombre}" class="player-card__img">
      <div class="player-card__body">
        <span class="player-card__number">#${player.dorsal}</span>
        <h3 class="player-card__name">${player.nombre}</h3>
        <p class="player-card__position">${player.posicion}</p>
      </div>
    </article>
  `).join('');

  // Eventos para abrir modal
  document.querySelectorAll('.player-card').forEach(card => {
    card.addEventListener('click', openModal);
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') openModal(e);
    });
  });
}

/* =====================
    LÓGICA DEL MODAL
===================== */
function openModal(e) {
  const id = Number(e.currentTarget.dataset.id);
  const player = players.find(p => p.id === id);

  if (!player) return;

  // Rellenar contenido
  modalImg.src = `../${player.foto}`;
  modalName.textContent = player.nombre;
  modalPosition.textContent = player.posicion;
  modalNumber.textContent = player.dorsal;
  modalAge.textContent = `${player.edad} años`;
  modalHeight.textContent = player.altura;
  modalDescription.textContent = player.descripcion;

  // Mostrar visualmente
  modal.classList.add('modal--open');
  // Cambiar estado ARIA
  modal.setAttribute('aria-hidden', 'false');

  // FOCO: Mover foco al botón cerrar para accesibilidad
  if (closeModalBtn && typeof closeModalBtn.focus === 'function') {
    setTimeout(() => closeModalBtn.focus(), 100);
  }
}


function closeModal() {
  if (!modal) return;

  // 1. Quitar clase visual
  modal.classList.remove('modal--open');

  // 2. FOCO: Mover el foco fuera del modal ANTES de usar aria-hidden
  // Esto evita el error: "Blocked aria-hidden on an element because its descendant retained focus"
  document.body.focus();

  // 3. Ocultar a lectores de pantalla
  modal.setAttribute('aria-hidden', 'true');
}

/* =====================
    EVENTOS DE CIERRE
===================== */
if (closeModalBtn) {
  closeModalBtn.addEventListener('click', closeModal);
}

// Cerrar al hacer clic fuera del contenido (en el fondo oscuro)
if (modal) {
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });
}

// Cerrar con tecla Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && modal.classList.contains('modal--open')) {
    closeModal();
  }
});
