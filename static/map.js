"use strict;"

function initMap() {
    const detroitCoords = {
        lat: 42.43334,
        lng: -83.12840
    }};

const basicMap = new google.maps.Map(
    document.querySelector('#map'),
    {
    center: detroitCoords,
    zoom: 3
    }
);