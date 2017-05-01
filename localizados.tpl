<!DOCTYPE html>
<html>
  <head>
    <title>Localizados</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <link rel="stylesheet" href="/static/styles/layout.css" type="text/css">
    <style>
      /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
      #map {
        height: 75%;
        width: 100%
      }
      /* Optional: Makes the sample page fill the window. */
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <div class="wrapper row1">
      <header id="header" class="drop">
        <div id="hgroup">
          <h1><a href="/">Geoscores</a></h1>
          <h2>Geolocalización de partidos de la liga</h2>
        </div>
        <nav>
          <ul>
            <li><a href="/">Inicio</a></li>
            <li><a href="/clasificacion/ligasantander">Liga Santander</a></li>
            <li><a href="/clasificacion/liga123">Liga 1|2|3</a></li>
            <li><a href="/localizalo">Localizalo</a></li>
          </ul>
        </nav>
      </header>
    </div>
    <div id="map"></div>
    <script>
    function initMap() {
      var lat = {{!lat}};
      var lng = {{!lng}};
      var local = {{!local}};
      var visitante = {{!visitante}};
      var fecha = {{!fecha}};
      var hora = {{!hora}};
      var resultado = {{!resultado}};
      var spain =  new google.maps.LatLng(39.996775,-4.203790);
      var map;
      var features = [];
      map = new google.maps.Map(document.getElementById('map'), {
        zoom:6,
        center: spain,
        mapTypeId: 'roadmap'
      });
      var marker, i;
      var infowindow = new google.maps.InfoWindow();

      for (i = 0; i < local.length; i++){
        marker = new google.maps.Marker({
          icon: '/static/images/soccer.png',
          position: new google.maps.LatLng(lat[i],lng[i]),
          map:map
      });

        google.maps.event.addListener(marker,'click',(function(marker,i){
          return function(){
            infowindow.setContent('<div id="content">'+
      '<p align="center">'+local[i]+' vs '+visitante[i]+'</p>'+
      '<p align="center">'+fecha[i]+' a las '+hora[i]+'</p>'+
      '<p align="center">'+resultado[i]+'</p>'+
      '<p><a class="twitter-share-button" href="https://twitter.com/intent/tweet">Tweet</a></p>'+
      '</div>');
            infowindow.open(map,marker);
          }
        })(marker,i));

      }
    }
    google.maps.event.addDomListener(window,'load',initMap);
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBSwXLHcj1T9gp7yIxVqS6dyVJc_t7F-Zw&callback=initMap">
    </script>
    <div class="wrapper row3">
      <footer id="footer" class="clear">
        <p class="fl_left"><a href="http://www.twitter.com/davtincas">Twitter Desarrollador</a></p>
        <p class="fl_right">Web para LM</p>
      </footer>
    </div>
  </body>
  </html>