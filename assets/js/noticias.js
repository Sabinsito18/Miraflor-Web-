const CLUB_NAME = 'Cultural Deportiva Miraflor';
const newsList = document.getElementById('newsList');
const newsStatus = document.getElementById('newsStatus');

function parseMatchDate(value) {
  return new Date(value.replace(' ', 'T'));
}

function formatNewsDate(value) {
  return new Intl.DateTimeFormat('es-ES', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  }).format(parseMatchDate(value));
}

function getOpponent(match) {
  return match.local === CLUB_NAME ? match.visitante : match.local;
}

function getVenue(match) {
  return match.local === CLUB_NAME ? 'en casa' : 'a domicilio';
}

function getResultType(match) {
  const miraflorGoals = match.local === CLUB_NAME ? match.goles_local : match.goles_visitante;
  const rivalGoals = match.local === CLUB_NAME ? match.goles_visitante : match.goles_local;

  if (miraflorGoals > rivalGoals) return 'victoria';
  if (miraflorGoals < rivalGoals) return 'derrota';
  return 'empate';
}

function getScore(match) {
  return `${match.goles_local}-${match.goles_visitante}`;
}

function getHeadline(match) {
  const opponent = getOpponent(match);
  const resultType = getResultType(match);

  if (resultType === 'victoria') {
    return `El Miraflor gana ante ${opponent}`;
  }

  if (resultType === 'derrota') {
    return `El Miraflor cae ante ${opponent}`;
  }

  return `El Miraflor empata ante ${opponent}`;
}

function getSummary(match) {
  const opponent = getOpponent(match);
  const venue = getVenue(match);
  const score = getScore(match);
  const resultType = getResultType(match);

  if (resultType === 'victoria') {
    return `El A.C.D. Miraflor firmó una victoria ${venue} frente a ${opponent}. El marcador final fue ${score}, en un partido en el que el equipo supo competir, aprovechar sus momentos y proteger la ventaja hasta el final.`;
  }

  if (resultType === 'derrota') {
    return `El A.C.D. Miraflor no pudo sumar ${venue} frente a ${opponent}. El encuentro terminó ${score}; el equipo lo intentó durante la jornada, pero el rival fue más eficaz en las áreas.`;
  }

  return `El A.C.D. Miraflor repartió puntos ${venue} frente a ${opponent}. El ${score} refleja un partido igualado, con alternativas y una respuesta competitiva del equipo hasta el último tramo.`;
}

function renderNews(matches) {
  if (!newsList) return;

  const playedMatches = matches
    .filter((match) => match.estado === 'jugado')
    .sort((a, b) => parseMatchDate(b.fecha) - parseMatchDate(a.fecha));

  if (newsStatus) {
    newsStatus.textContent = `${playedMatches.length} crónicas generadas automáticamente desde los partidos jugados.`;
  }

  if (playedMatches.length === 0) {
    newsList.innerHTML = '<p class="news-empty">Todavía no hay partidos jugados para generar noticias.</p>';
    return;
  }

  newsList.innerHTML = playedMatches.map((match) => `
    <article class="info__card news-card news-card--generated">
      <div class="news-card__image news-card__image--generated">
        <span>J${match.jornada}</span>
      </div>
      <div class="news-card__content">
        <span class="news-card__date">${formatNewsDate(match.fecha)}</span>
        <h2>${getHeadline(match)}</h2>
        <p class="news-card__score">${match.local} ${getScore(match)} ${match.visitante}</p>
        <p>${getSummary(match)}</p>
      </div>
    </article>
  `).join('');
}

fetch('/api/partidos')
  .then((response) => {
    if (!response.ok) throw new Error('API no disponible');
    return response.json();
  })
  .then(renderNews)
  .catch(() => {
    if (newsStatus) {
      newsStatus.textContent = 'Arranca server.py para generar las noticias desde la base de datos.';
    }
    if (newsList) {
      newsList.innerHTML = '<p class="news-empty">No se pudo conectar con la base de datos.</p>';
    }
  });
