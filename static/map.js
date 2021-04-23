"use strict;"

function initMap() {
    const detroitCoords = {
        lat: 42.43334,
        lng: -83.12840
    };

    const basicMap = new google.maps.Map(
        document.querySelector('#map'),
        {
        center: detroitCoords,
        zoom: 4,
        zoomControl: true,
        panControl: false,
        streetViewControl: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP
        }
    );
}

const wapoInfo = new google.maps.InfoWindow();

// Retrieving the information with AJAX.
//
$.get('/api/map', (wapost) => {
  for (const wapo of wapost) {
    // Define the content of the infoWindow
    const wapoInfoContent = (`
      <div class="window-content">

        <ul class="wapo-info">
          <li><b>Name: </b>${wapost.name}</li>
          <li><b>Date of Incident: </b>${wapost.date}</li>
          <li><b>Manner of Death: </b>${wapost.manner_of_death}</li>
          <li><b>Reportedly Armed: </b>${wapost.allegedly_armed}</li>
          <li><b>Age: </b>${wapost.age}</li>
          <li><b>Gender: </b>${wapost.gender}</li>
          <li><b>Race: </b>${wapost.race}</li>
          <li><b>City: </b>${wapost.city}</li>
          <li><b>State: </b>${wapost.state}</li>
          <li><b>Signs of Mental Illness: </b>${wapost.signs_of_mental_illness}</li>
          <li><b>Reported Threat Level: </b>${wapost.alleged_threat_level}</li>
          <li><b>Reportedly Fleeing: </b>${wapost.allegedly_fleeing}</li>
          <li><b>Body Camera Present: </b>${wapost.body_camera}</li>
          <li><b>Longitude: </b>${wapost.longitude}</li>
          <li><b>Latitude: </b>${wapost.latitude}</li>
        </ul>
      </div>
    `);

    const wapoMarker = new google.maps.Marker({
      position: {
        lat: wapost.latitude,
        lng: wapost.longitude
      },
      title: `Data ID: ${wapo.data_id}`,
      map: map,
    });

    wapoMarker.addListener('click', () => {
      wapoInfo.close();
      wapoInfo.setContent(wapoInfoContent);
      wapoInfo.open(map, wapoMarker);
    });
  }
});