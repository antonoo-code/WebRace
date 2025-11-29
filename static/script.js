const form = document.getElementById("startgame");
const nameInput = document.getElementById("namebox");
const flightOptions = document.getElementById("flight_options");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = nameInput.value;
  const response = await fetch("/game?name=" + encodeURIComponent(name), {
    method: "POST",
  });
  const data = await response.json();

  const ul = flightOptions.querySelector("ul");
  data.stats.flight_options.forEach((flight) => {
    const li = document.createElement("li");
    li.textContent = flight.icao + ", " + flight.name;
    ul.appendChild(li);
  });
});
