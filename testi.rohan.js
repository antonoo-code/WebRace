"use strict";

const map = L.map("map", {tap: false});
L.tileLayer("https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", {
  maxZoom: 20,
  subdomains: ["mto", "mt1", "mt2", "mt3"],
}).addTo(map)
map.setView([60, 24], 7);