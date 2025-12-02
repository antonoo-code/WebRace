//Tästä alkaa Anton lentolista js
const form = document.getElementById("startgame");
const nameInput = document.getElementById("namebox");
const flightOptions = document.getElementById("flight_options");
const range = document.getElementById("range");

//function display_playerRange(data) {
// const a = flightOptions.querySelector("range");
//const ra = document.createElement("ra");
// a.textContent = data.stats.player_range;
//a.appendChild(ra);
//}

function display_flightoptions(data) {
  const ul = flightOptions.querySelector("ul");
  data.stats.flight_options.forEach((flight) => {
    const li = document.createElement("li");
    li.textContent = flight.icao + ", " + flight.name;
    ul.appendChild(li);
  });
  ///display_playerRange(data);
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
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
      display_flightoptions(data);
    }
  });
});

//Tähä loppuu Anton lentolista js

// Kartta(Rohan)
const map = L.map("map", { tap: false });
L.tileLayer("https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", {
  maxZoom: 20,
  subdomains: ["mt0", "mt1", "mt2", "mt3"],
}).addTo(map);
map.setView([60, 24], 7);
