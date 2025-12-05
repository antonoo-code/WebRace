//Tästä alkaa Anton lentolista js
const form = document.getElementById("startgame");
const nameInput = document.getElementById("namebox");
const flightOptions = document.getElementById("flight_options");
const range = document.getElementById("range");

function display_flightoptions(data) {
  const ul = flightOptions.querySelector("ul");
  ul.innerHTML = "";
  data.stats.flight_options.forEach((flight) => {
    const li = document.createElement("li");
    li.textContent = flight.icao + ", " + flight.name;
    ul.appendChild(li);
  });
  range.innerHTML = String(data.stats.player_range);
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
  //eero nappi
  window.throwDice = async function () {
    fetch(`/game?action=dice&id=${id}`, {
      method: "PUT",
    });
  };

  window.charge = async function () {
    const response = await fetch(`/game?action=charge&id=${id}`, {
      method: "PUT",
    });
    let data = await response.json();
    display_flightoptions(data);
  };
});

//Tähä loppuu Anton lentolista js
