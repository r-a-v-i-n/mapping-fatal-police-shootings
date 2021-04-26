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
    // make a .get request to the server
    // server will return WaPo data as json
    $.get('/api/map', (data) => {
     
      const wapoInfo = new google.maps.InfoWindow();
      for (const wapost of data) {
        if (wapost.latitude === null) {
          continue;
        }
        const wapoMarker = new google.maps.Marker({
        position: {
          lat: wapost.latitude,
          lng: wapost.longitude
        },
        title: `Data ID: ${wapost.data_id}`,
        map: basicMap,
      });
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
      wapoMarker.addListener('click', () => {
        wapoInfo.close();
        wapoInfo.setContent(wapoInfoContent);
        wapoInfo.open(basicMap, wapoMarker);
      });
      }
    })

}



  //   # option 1:
  //   # use geolocation
  //   # (not a google maps things, it's built into js)
  //   # - this will ask the user "can I know where you are"
  //   # this will return the result as lat-long coords
  //   # which can be plugged into map
  //     look at the geolocation api in JS

  //   # option 2:
  //   # use what's stored about the user
  //   # initMap --> ajax request --> geocoder --> ajax --> map logic
  //   # lots o nesting
  //   # make an ajax request to the server to get user info from db
  //   # use google maps geocoder
  //     give the string of user loc to the geocoder, geocoder produces lat-long
  //     continue on with code I have, uses the same logic