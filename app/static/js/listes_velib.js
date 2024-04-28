let fav = document.querySelectorAll(".fav");

console.log(fav);

for (let i = 0; i < fav.length; i++) {
  let isGreen = false; // Variable pour suivre l'état

  fav[i].addEventListener("click", function (event) {
    let current = event.currentTarget;

    // Si c'est vert, changer en rouge
    if (isGreen) {
      current.style.backgroundColor = "red";
      isGreen = false;
    } else {
      // Sinon, changer en vert
      current.style.backgroundColor = "green";
      isGreen = true;
    }
  });
}

// gestion du map

let coordonnees_geo = {
  lon: 2.4865807592869,
  lat: 48.871256519012,
};
var map = L.map("map").setView([48.8566, 2.3522], 13);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

var marker = L.marker([coordonnees_geo.lat, coordonnees_geo.lon]).addTo(map);

var popupContent = `
<div class="popup" style="display: flex; flex-direction: column; gap: 20px; width: 300px; border-radius: 25px;">
<p style="text-align: center;">Infos</p>
<div class="details" style="display: flex; flex-direction: column; gap: 10px;">
  <div style="height: 35px; background: rgb(224, 219, 219); display: flex; align-items: center;">
    <ion-icon name="location-outline"></ion-icon>
    <span style="text-align: center;">Benjamin Godard - Victor Hugo</span>
  </div>
  <div style="height: 35px; background: rgb(224, 219, 219); display: flex; align-items: center;">
    <img src="../static/images/Bike_meca3x.png" alt="" style="width: 25px;" />
    <span style="text-align: center;">10 Vélib' mécanique(s)</span>
  </div>
  <div style="height: 35px; background: rgb(224, 219, 219); display: flex; align-items: center;">
    <img src="../static/images/Bike_elec3x.png" alt="" style="width: 25px;" />
    <span style="text-align: center;">5 Vélib' électrique(s)</span>
  </div>
  <div style="height: 35px; background: rgb(224, 219, 219); display: flex; align-items: center;">
    <img src="../static/images/borne_velo_bleu2x.png" alt="" style="width: 25px;" />
    <span style="text-align: center;">2 place(s)</span>
  </div>
</div>
<div class="favorite_button" style="display: flex; align-items: center; gap: 5px; cursor: pointer;">
  <a href="#" style="text-decoration: none; color: black;">Ajouter aux favoris</a>
  <ion-icon name="heart-outline"></ion-icon>
</div>
</div>

`;

marker
  .bindPopup(popupContent, {
    className: "custom-popup-style",
  })
  .openPopup();
