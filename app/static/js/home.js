var map = L.map("map").setView([48.8566, 2.3522], 13);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

coordinates.forEach(function (coord) {
  var marker = L.marker([coord.lat, coord.lon]).addTo(map);

  var popupContent = `
    <div class="popup" style="display: flex; flex-direction: column; gap: 20px; width: 300px; border-radius: 25px;">
      <p style="text-align: center;font-size: 16px;font-weight: bold; margin: 10px;">Infos</p>
      <div class="details" style="display: flex; flex-direction: column; gap: 10px;">
        <div style="height: 35px; background: rgb(224, 219, 219); display: flex; align-items: center; ">
          <ion-icon name="location-outline"></ion-icon>
          <span style="margin: auto;;"><b>${coord.name}</b></span>
        </div>
        <div style="height: 35px; background: rgb(224, 219, 219); display: flex; align-items: center;">
          <img src="../static/images/Bike_meca3x.png" alt="" style="width: 25px;margin: 0 10px;" />
          <span style="text-align: center;"><b style="margin: 0 10px;">${coord.mechanical}</b> Vélib' mécanique(s)</span>
        </div>
        <div style="height: 35px; background: rgb(224, 219, 219); display: flex; align-items: center;">
          <img src="../static/images/Bike_elec3x.png" alt="" style="width: 25px;margin: 0 10px;" />
          <span style="text-align: center;"><b style="margin: 0 10px;">${coord.ebike}</b> Vélib' électrique(s)</span>
        </div>
        <div style="height: 35px; background: rgb(224, 219, 219); display: flex; align-items: center;">
          <img src="../static/images/borne_velo_bleu2x.png" alt="" style="width: 25px;margin: 0 10px;" />
          <span style="text-align: center;"><b style="margin: 0 10px;">${coord.numdocksavailable}</b> place(s)</span>
        </div>
      </div>
      <div class="favorite_button" style="display: flex; align-items: center; gap: 5px; cursor: pointer;">
      <form action="/addname" method="post">
      <input type="hidden" name="station_id" value="${coord.stationcode}">
      <input type="hidden" name="station_name" value="${coord.name}">
      <button type="submit" class='fav' style="background: #008B9F;color: white;height: 35px;border: none;border-radius: 4px;width: 150px;">Ajouter aux favoris</button>
    </form>
        <ion-icon name="heart-outline"></ion-icon>
      </div>
    </div>
  `;

  marker.bindPopup(popupContent, {
    className: "custom-popup-style",
  });
});

let pseudo = document.querySelector(".pseudo");
let profilSetting = document.querySelector(".profil-setting");
let profilSettingResponsiv = document.querySelector(
  ".profil-setting-responsiv"
);
let close = document.querySelector(".profil-setting .close");
let closeResponsiv = document.querySelector(
  ".profil-setting-responsiv .close-responsiv"
);
let menuBurger = document.querySelector(".menu-burger");

let moreEditDel = document.querySelector(".more-edit-del");
let moreBtn = document.querySelector(".button-more .more-btn");
let moreEditDelClose = document.querySelector(
  ".more-edit-del .more-edit-del-close"
);

pseudo.addEventListener("click", function () {
  profilSetting.classList.toggle("active");
});

close.addEventListener("click", function () {
  profilSetting.classList.remove("active");
});

menuBurger.addEventListener("click", function () {
  profilSettingResponsiv.classList.toggle("active");
});

closeResponsiv.addEventListener("click", function () {
  profilSettingResponsiv.classList.remove("active");
});

moreBtn.addEventListener("click", function () {
  moreBtn.style.display = "none";
  moreEditDel.classList.toggle("active");
});

let fav = document.querySelectorAll(".fav");

console.log(fav);

for (let i = 0; i < fav.length; i++) {
  let isGreen = false;

  fav[i].addEventListener("click", function (event) {
    let current = event.currentTarget;

    if (isGreen) {
      current.style.backgroundColor = "red";
      isGreen = false;
    } else {
      current.style.backgroundColor = "green";
      isGreen = true;
    }
  });
}
