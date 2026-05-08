const STORAGE_KEY = "visitas";
const MAX_DAYS_WITHOUT_FINCA = 60;

const form = document.getElementById("visit-form");
const historyList = document.getElementById("history-list");
const fincaStatus = document.getElementById("finca-status");
const dateInput = document.getElementById("date");

function getVisits() {
  const raw = localStorage.getItem(STORAGE_KEY);
  return raw ? JSON.parse(raw) : [];
}

function saveVisits(visits) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(visits));
}

function formatDate(dateString) {
  const date = new Date(`${dateString}T00:00:00`);
  return new Intl.DateTimeFormat("es-ES", { dateStyle: "long" }).format(date);
}

function daysBetween(fromDate, toDate = new Date()) {
  const from = new Date(`${fromDate}T00:00:00`);
  const to = new Date(toDate);
  const msPerDay = 1000 * 60 * 60 * 24;
  return Math.floor((to - from) / msPerDay);
}

function renderHistory() {
  const visits = getVisits();

  if (!visits.length) {
    historyList.innerHTML = "<li>No hay visitas registradas todavía.</li>";
    return;
  }

  historyList.innerHTML = visits
    .sort((a, b) => b.date.localeCompare(a.date))
    .map(
      (visit) =>
        `<li><strong>${visit.location}</strong> · ${formatDate(visit.date)}</li>`
    )
    .join("");
}

function renderFincaStatus() {
  const visits = getVisits();
  const fincaVisits = visits
    .filter((v) => v.location === "finca")
    .sort((a, b) => b.date.localeCompare(a.date));

  if (!fincaVisits.length) {
    fincaStatus.className = "card status warning";
    fincaStatus.innerHTML = `
      <h2>Estado de finca</h2>
      <p><strong>Sin visitas registradas.</strong> Registra una visita para activar el control de 2 meses.</p>
    `;
    return;
  }

  const lastVisit = fincaVisits[0].date;
  const days = daysBetween(lastVisit);

  if (days > MAX_DAYS_WITHOUT_FINCA) {
    fincaStatus.className = "card status warning";
    fincaStatus.innerHTML = `
      <h2>Estado de finca</h2>
      <p><strong>⚠️ Alerta:</strong> Han pasado ${days} días desde la última visita a la finca.</p>
      <small>Última visita: ${formatDate(lastVisit)}</small>
    `;
    return;
  }

  fincaStatus.className = "card status ok";
  fincaStatus.innerHTML = `
    <h2>Estado de finca</h2>
    <p><strong>✅ Todo en orden.</strong> Han pasado ${days} días desde la última visita a la finca.</p>
    <small>Última visita: ${formatDate(lastVisit)}</small>
  `;
}

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const location = document.getElementById("location").value;
  const date = dateInput.value;

  const visits = getVisits();
  visits.push({ location, date });

  saveVisits(visits);
  renderHistory();
  renderFincaStatus();
  form.reset();
  dateInput.valueAsDate = new Date();
});

function init() {
  dateInput.valueAsDate = new Date();
  renderHistory();
  renderFincaStatus();
}

init();
