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
  range.innerHTML = String(data.stats.player_range);
  goal.innerHTML = String(data.stats.goal_airport_name);
  distance2goal.innerHTML = String(data.stats.goal_distance);
  currentAirport.innerHTML = data.stats.current_airport_name;
  if (data.stats.can_supercharge === true) {
    console.log("supercharging");
    chargeButton.innerText = "Supercharge";
  } else {
    console.log("charging");
    chargeButton.innerText = "Lataa";
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
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
