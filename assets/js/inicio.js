const HOME_CLUB_NAME = 'Cultural Deportiva Miraflor';
const homeNextMatch = document.getElementById('homeNextMatch');
const homeLatestNews = document.getElementById('homeLatestNews');

function parseHomeDate(value) {
  return new Date(value.replace(' ', 'T'));
}

function formatHomeDate(value) {
  const hasTime = !value.endsWith('00:00');
  return new Intl.DateTimeFormat('es-ES', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: hasTime ? '2-digit' : undefined,
    minute: hasTime ? '2-digit' : undefined
  }).format(parseHomeDate(value));
}

function getHomeOpponent(match) {
  return match.local === HOME_CLUB_NAME ? match.visitante : match.local;
}

function getHomeVenue(match) {
  return match.local === HOME_CLUB_NAME ? 'Local' : 'Visitante';
}

function getHomeResultType(match) {
  const miraflorGoals = match.local === HOME_CLUB_NAME ? match.goles_local : match.goles_visitante;
  const rivalGoals = match.local === HOME_CLUB_NAME ? match.goles_visitante : match.goles_local;

  if (miraflorGoals > rivalGoals) return 'victoria';
  if (miraflorGoals < rivalGoals) return 'derrota';
  return 'empate';
}

function getHomeNewsHeadline(match) {
  const opponent = getHomeOpponent(match);
  const resultType = getHomeResultType(match);

  if (resultType === 'victoria') return `El Miraflor gana ante ${opponent}`;
  if (resultType === 'derrota') return `El Miraflor cae ante ${opponent}`;
  return `El Miraflor empata ante ${opponent}`;
}

function getHomeNewsSummary(match) {
  const opponent = getHomeOpponent(match);
  const score = `${match.goles_local}-${match.goles_visitante}`;
  const venue = match.local === HOME_CLUB_NAME ? 'en casa' : 'a domicilio';
  const resultType = getHomeResultType(match);

  if (resultType === 'victoria') {
    return `Victoria ${venue} frente a ${opponent}. El equipo compitió con intensidad y cerró el partido con un ${score}.`;
  }

  if (resultType === 'derrota') {
    return `Derrota ${venue} ante ${opponent}. El Miraflor lo intentó, pero el rival fue más eficaz y el marcador acabó ${score}.`;
  }

  return `Empate ${venue} frente a ${opponent}. El ${score} dejó un encuentro igualado y peleado hasta el final.`;
}

function renderHomeNextMatch(matches) {
  if (!homeNextMatch) return;

  const nextMatch = matches
    .filter((match) => match.estado === 'por_jugar')
    .sort((a, b) => parseHomeDate(a.fecha) - parseHomeDate(b.fecha))[0];

  if (!nextMatch) {
    homeNextMatch.innerHTML = '<p>No hay partidos programados.</p>';
    return;
  }

  homeNextMatch.innerHTML = `
    <p><strong>Jornada ${nextMatch.jornada}</strong></p>
    <p>${nextMatch.local} - ${nextMatch.visitante}</p>
    <p><strong>Fecha:</strong> ${formatHomeDate(nextMatch.fecha)}</p>
    <p><strong>Campo:</strong> ${getHomeVenue(nextMatch)}</p>
  `;
}

function renderHomeLatestNews(matches) {
  if (!homeLatestNews) return;

  const latestMatch = matches
    .filter((match) => match.estado === 'jugado')
    .sort((a, b) => parseHomeDate(b.fecha) - parseHomeDate(a.fecha))[0];

  if (!latestMatch) {
    homeLatestNews.innerHTML = '<p>Todavía no hay noticias de partidos jugados.</p>';
    return;
  }

  homeLatestNews.innerHTML = `
    <p class="home-news__date">${formatHomeDate(latestMatch.fecha)}</p>
    <h3>${getHomeNewsHeadline(latestMatch)}</h3>
    <p class="home-news__score">${latestMatch.local} ${latestMatch.goles_local}-${latestMatch.goles_visitante} ${latestMatch.visitante}</p>
    <p>${getHomeNewsSummary(latestMatch)}</p>
  `;
}

function renderHome(matches) {
  renderHomeNextMatch(matches);
  renderHomeLatestNews(matches);
}

fetch('/api/partidos')
  .then((response) => {
    if (!response.ok) throw new Error('API no disponible');
    return response.json();
  })
  .then(renderHome)
  .catch(() => {
    const fallbackMatches = [
      {
        jornada: 30,
        fecha: '2026-05-10 17:00',
        local: HOME_CLUB_NAME,
        visitante: 'Nuevo Boadilla',
        goles_local: 1,
        goles_visitante: 2,
        estado: 'jugado'
      },
      {
        jornada: 31,
        fecha: '2026-05-17 18:00',
        local: 'Ciudad de Getafe SC',
        visitante: HOME_CLUB_NAME,
        goles_local: null,
        goles_visitante: null,
        estado: 'por_jugar'
      }
    ];

    renderHome(fallbackMatches);
  });
