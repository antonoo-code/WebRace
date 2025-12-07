//Tästä alkaa Anton lentolista js
const form = document.getElementById("startgame");
const nameInput = document.getElementById("namebox");
const flightOptions = document.getElementById("flight_options");
const range = document.getElementById("range");
const goal = document.getElementById("maali");
const distance2goal = document.getElementById("matka");
const chargeButton = document.getElementById("chargebutton");
const currentAirport = document.getElementById("current_airport");

function display_flightoptions(data) {
  if (data.stats.goal_reached_by === "npc") {
    window.location.href = "/static/victory.html?winner=npc";
  } else if (data.stats.goal_reached_by === "player") {
    window.location.href = "/static/victory.html?winner=player";
  }
  const ul = flightOptions.querySelector("ul");
  ul.innerHTML = "";
  data.stats.flight_options.forEach((flight) => {
    const li = document.createElement("li");
    li.textContent =
      flight.icao + ", " + flight.name + " (" + flight.range + " Km)";
    ul.appendChild(li);
  });
  range.innerHTML = String("Range: " + data.stats.player_range.toFixed(0));
  goal.innerHTML = String("Maali: " + data.stats.goal_airport_name);
  distance2goal.innerHTML = String("Matka maaliin: " + data.stats.goal_distance.toFixed(0));
  currentAirport.innerHTML = "Sijainti: " + data.stats.current_airport_name;
  if (data.stats.can_supercharge === true) {
    console.log("supercharging");
    chargeButton.innerText = "Supercharge";
  } else {
    console.log("charging");
    chargeButton.innerText = "Lataa";
  }
  updateMap(data);
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  document.getElementById("start").style.display = "none";
  let range = 0;
  const name = nameInput.value;
  const response = await fetch("/game?name=" + encodeURIComponent(name), {
    method: "POST",
  });
  console.log(response);
  let data = await response.json();
  const id = data.id;

  display_flightoptions(data);
  const ul = flightOptions.querySelector("ul");
  ul.addEventListener("click", async (e) => {
    if (e.target.tagName === "LI") {
      icao = e.target.textContent.split(",")[0];
      ul.innerHTML = "";
      const response = await fetch(`/game?action=fly&id=${id}&icao=${icao}`, {
        method: "PUT",
      });
      data = await response.json();
      range = data.player_range;
      display_flightoptions(data);
    }
  });

  window.charge = async function () {
    const response = await fetch(`/game?action=charge&id=${id}`, {
      method: "PUT",
    });
    let data = await response.json();
    console.log(data);
    range = data.player_range;
    display_flightoptions(data);
  };

  window.findNPC = async function () {
    const response = await fetch(`/game?action=locationQuery&id=${id}`, {
      method: "PUT",
    });
    let data = await response.json();
    console.log(data);
    range = data.player_range;
    display_flightoptions(data);
    const div = document.getElementById("logit");
    div.innerHTML =
      "Möttösen sijainti on " +
      data.stats.npc_airport.name +
      "<br>" +
      div.innerHTML;
  };

  window.throwDice = async function () {
    const response = await fetch(`/game?action=dice&id=${id}`, {
      method: "PUT",
    });
    let data = await response.json();
    console.log(data);
    //range = data.player_range;
    display_flightoptions(data);
    const div = document.getElementById("logit");
    div.innerHTML = data.stats.dice_message + "<br>" + div.innerHTML;
  };
});

//Tähä loppuu Anton lentolista js


// Kartta alkaa tästä (Rohan)

// Hakee lentokentan koordinaatit
async function coordinates(icao) {
  const response = await fetch(`/airport?icao=${icao}`);
  const data = await response.json();
  return [data.latitude_deg, data.longitude_deg];
}

// Päivittää kartan
async function updateMap(data) {
  if (!window.gameMap) return;

  // Poista vanhat merkit
  window.gameMap.eachLayer((layer) => {
    if (layer instanceof L.Marker) {
      window.gameMap.removeLayer(layer);
    }
  });

  const stats = data.stats;
  // Lisää pelaajan sijainnin
  if (stats.location) {
    const playerCoords = await coordinates(stats.location);

    if (playerCoords) {
      const playerMarker = L.marker(playerCoords, {
        icon: L.divIcon({
          className: "player-marker",
          html: "📍",
          iconSize: [25,25]
        })
      }).addTo(window.gameMap);

      playerMarker.bindPopup(`<b>${stats.current_airport_name}</b><br>Sijaintisi`).openPopup();
      window.gameMap.setView(playerCoords, 7);
    }
  }

  // Lentovaihtoehdot kartalle
  if (stats.flight_options) {
    for (const airport of stats.flight_options) {
      if (airport.icao) {
        const coords = await coordinates(airport.icao);

        if (coords) {
          const airportMarker = L.marker(coords, {
            icon: L.divIcon({
              className: "airport-marker",
              html: '✈',
              iconSize: [25, 25]
            })
          }).addTo(window.gameMap);

          airportMarker.bindPopup(`
          <b>${airport.name}</b><br>
          ICAO: ${airport.icao}<br>
          Etäisyys: ${airport.range} km`);
        }
      }
    }
  }

  // Möttösen sijainti
  if (stats.npc_airport && stats.npc_airport.icao) {
    const mottonenCoords = await coordinates(stats.npc_airport.icao);

    if (mottonenCoords) {
      const mottonenMarker = L.marker(mottonenCoords, {
        icon: L.divIcon({
          className: "mottonen-marker",
          html: "👤",
          iconSize: [25, 25]
        })
      }).addTo(window.gameMap);

      mottonenMarker.bindPopup(`<b>${stats.npc_airport.name}</b><br>Möttösen sijainti`).openPopup();
      window.gameMap.setView(mottonenCoords, 7);}
  }}

// tähän loppuu kartta (rohan)