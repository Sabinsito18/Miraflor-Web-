const matchesTable = document.getElementById('matchesTable');
const calendarSource = document.getElementById('calendarSource');

function formatDate(value) {
  const date = new Date(value.replace(' ', 'T'));
  const hasTime = !value.endsWith('00:00');
  const formatted = new Intl.DateTimeFormat('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: hasTime ? '2-digit' : undefined,
    minute: hasTime ? '2-digit' : undefined
  }).format(date);

  return formatted.replace(',', '');
}

function renderMatches(matches) {
  if (!matchesTable) return;

  matchesTable.innerHTML = matches.map((match) => {
    const result = match.estado === 'jugado'
      ? `${match.goles_local}-${match.goles_visitante}`
      : '-';
    const statusClass = match.estado === 'jugado'
      ? 'match-status--played'
      : 'match-status--upcoming';
    const statusText = match.estado === 'jugado' ? 'Jugado' : 'Por jugar';

    return `
      <tr>
        <td>${match.jornada}</td>
        <td>${formatDate(match.fecha)}</td>
        <td>${match.local} - ${match.visitante}</td>
        <td>${result}</td>
        <td><span class="match-status ${statusClass}">${statusText}</span></td>
      </tr>
    `;
  }).join('');

  if (calendarSource) {
    calendarSource.textContent = 'Datos cargados desde la base de datos local.';
  }
}

fetch('/api/partidos')
  .then((response) => {
    if (!response.ok) throw new Error('API no disponible');
    return response.json();
  })
  .then(renderMatches)
  .catch(() => {
    if (calendarSource) {
      calendarSource.textContent = 'Mostrando datos estáticos. Arranca server.py para usar la base de datos.';
    }
  });
