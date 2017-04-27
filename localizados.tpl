%include('header.tpl')
  <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <link rel="icon" type="image/png" href="/static/findit-ico.png">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Mapa</title>
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&signed_in=true"></script>
    <script>
  function initMap() {
    var lng = {{lng}};
    var lat = {{lat}};
    var local = {{local}}
    var visitante = {{visitante}}
    var fecha = {{fecha}}
    var hora = {{hora}}
    var resultado = {{resultado}}
    var uluru = {lat:40.1217685, lng:-8.2011237.6};
    var mapOptions = {zoom: 10, center: uluru}
    var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
    var marker, i;
    var infowindow = new google.maps.InfoWindow();

    for (i=0; i < local.length; i++) {
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(lat[i], lng[i]),
        map: map
      });
      google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infowindow.setContent(
            '<div id="content">'+
            '<p>'+local[i]+' vs '+visitante[i]+'</p>'+
            '<p>'+fecha[i]+' a las '+hora[i]+'</p>'+
            '<p>'+resultado[i]+'</p>'+
            '</div>'
            );
          infowindow.open(map, marker);
        }
      })(marker, i));
    }
  }
  google.maps.event.addDomListener(window, 'load', initialize);
  </script>
  <script async defer
  src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBSwXLHcj1T9gp7yIxVqS6dyVJc_t7F-Zw&callback=initMap">
  </script>
  %include('foot.tpl')