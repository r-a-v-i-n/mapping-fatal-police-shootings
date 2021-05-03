"use strict;"

function initMap() {
    const centerCoords = {
        lat: 48.2283,
        lng: -98.5795
    };

    const basicMap = new google.maps.Map(
        document.querySelector('#map'),
        {
        center: centerCoords,
        zoom: 3,
        styles: [
          { elementType: "geometry", stylers: [{ color: "#000000" }] },
          { elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
          { elementType: "labels.text.fill", stylers: [{ color: "#ffffff" }] },
          {
            featureType: "administrative.locality",
            elementType: "labels.text.fill",
            stylers: [{ color: "#ffffff" }],
          },
          {
            featureType: "poi",
            elementType: "labels.text.fill",
            stylers: [{ color: "#ffffff" }],
          },
          // {
          //   featureType: "poi.park",
          //   elementType: "geometry",
          //   stylers: [{ color: "#263c3f" }],
          // },
          // {
          //   featureType: "poi.park",
          //   elementType: "labels.text.fill",
          //   stylers: [{ color: "#6b9a76" }],
          // },
          // {
          //   featureType: "road",
          //   elementType: "geometry",
          //   stylers: [{ color: "#38414e" }],
          // },
          // {
          //   featureType: "road",
          //   elementType: "geometry.stroke",
          //   stylers: [{ color: "#212a37" }],
          // },
          // {
          //   featureType: "road",
          //   elementType: "labels.text.fill",
          //   stylers: [{ color: "#9ca5b3" }],
          // },
          {
            featureType: "road.highway",
            elementType: "geometry",
            stylers: [{ color: "#ffffff" }],
          },
          {
            featureType: "road.highway",
            elementType: "geometry.stroke",
            stylers: [{ color: "#1f2835" }],
          },
          {
            featureType: "road.highway",
            elementType: "labels.text.fill",
            stylers: [{ color: "#ffffff" }],
          },
          {
            featureType: "transit",
            elementType: "geometry",
            stylers: [{ color: "#2f3948" }],
          },
          {
            featureType: "transit.station",
            elementType: "labels.text.fill",
            stylers: [{ color: "#ffffff" }],
          },
          {
            featureType: "water",
            elementType: "geometry",
            stylers: [{ color: "#439D94" }],
          },
          {
            featureType: "water",
            elementType: "labels.text.fill",
            stylers: [{ color: "#ffffff" }],
          },
          {
            featureType: "water",
            elementType: "labels.text.stroke",
            stylers: [{ color: "#242f3e" }],
          },
        ],
        zoomControl: true,
        panControl: false,
        streetViewControl: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP
        
        }
    );
    
      // Create the search box and link it to the UI element.
    const input = document.getElementById("pac-input");
    const searchBox = new google.maps.places.SearchBox(input);
    basicMap.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
    // Bias the SearchBox results towards current map's viewport.
    basicMap.addListener("bounds_changed", () => {
      searchBox.setBounds(basicMap.getBounds());
    });
    let markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener("places_changed", () => {
      const places = searchBox.getPlaces();

      if (places.length == 0) {
        return;
      }
      // Clear out the old markers.
      markers.forEach((marker) => {
        marker.setMap(null);
      });
      markers = [];
      // For each place, get the icon, name and location.
      const bounds = new google.maps.LatLngBounds();
      places.forEach((place) => {
        if (!place.geometry || !place.geometry.location) {
          console.log("Returned place contains no geometry");
          return;
        }
        const icon = {
          url: place.icon,
          size: new google.maps.Size(71, 71),
          origin: new google.maps.Point(0, 0),
          anchor: new google.maps.Point(17, 34),
          scaledSize: new google.maps.Size(25, 25),
        };
        // Create a marker for each place.
        markers.push(
          new google.maps.Marker({
            map,
            icon,
            title: place.name,
            position: place.geometry.location,
          })
        );

        if (place.geometry.viewport) {
          // Only geocodes have viewport.
          bounds.union(place.geometry.viewport);
        } else {
          bounds.extend(place.geometry.location);
        }
      });
      basicMap.fitBounds(bounds);
    });

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

  // water - 99d7e3