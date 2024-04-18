let fav = document.querySelectorAll('.fav');

console.log(fav);

for (let i = 0; i < fav.length; i++) {
    let isGreen = false; // Variable pour suivre l'état

    fav[i].addEventListener('click', function (event) {
        let current = event.currentTarget;
        
        // Si c'est vert, changer en rouge
        if (isGreen) {
            current.style.backgroundColor = 'red';
            isGreen = false;
        } else { // Sinon, changer en vert
            current.style.backgroundColor = 'green';
            isGreen = true;
        }
    });
}





// gestion du map
        
let coordonnees_geo = {

    "lon":2.4865807592869,
    "lat":48.871256519012

}
var map = L.map('map').setView([48.8566, 2.3522], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var marker = L.marker([coordonnees_geo.lat, coordonnees_geo.lon]).addTo(map);


// {% for coord in coordinates %}
//     L.marker([{{ coord[0] }}, {{ coord[1] }}]).addTo(map);
// {% endfor %}

