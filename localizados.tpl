%include('header.tpl')
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
      var spain = new google.maps.LatLng(39.996775,-4.203790);
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
      '<form action="/tweet" method=post>'+
      '<input type="hidden" name="cuerpo" value="El '+local[i]+' vs '+visitante[i]+
      ' se juega/jugó el '+fecha[i]+' a las '+hora[i]+' con un resultado de '+resultado[i]+'."/>'+
      '<input type="submit" class="button" value="Twitit"/>'+
      '</form>'+
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
%include('foot.tpl')