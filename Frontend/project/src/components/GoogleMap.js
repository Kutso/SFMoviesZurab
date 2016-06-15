import React from "react";
import ReactDOM from "react-dom";

export default class GoogleMap extends React.Component {
  constructor(props){
    super(props);

    this.map = undefined;
    this.markers = [];
    this.infoWindow = undefined;
  }

  componentDidMount = (rootNode) => {
    const center = this.props.data.center;
    const thisNode = ReactDOM.findDOMNode(this);
    this.map = new google.maps.Map(thisNode, {
      center: center,
      zoomControl: false,
      streetViewControl: false,
      zoom: 12,
      maxZoom: 16,
      minZoom: 1
    });

    google.maps.event.addDomListener(window, 'resize', ()=> {
        this.map.setCenter(center);
    });
  }

  componentDidUpdate = () => {
    this.setMarkers();
  }

  panToPin = (obj) => {
    const infoTitle = "<h3>" + obj.address + "</h3>";
    const funFact = obj.funfact ? "<p>" + obj.funfact + "</p>" : "";

    this.infoWindow.setContent('<div class="InfoWindow">' + infoTitle + funFact + '</div>');
    this.infoWindow.open(this.map, this.markers[obj.index]);

    for (var i = 0; i < this.markers.length; i++) {
      this.markers[i].setAnimation(null);
    }
    this.markers[obj.index].setAnimation(google.maps.Animation.BOUNCE);

    this.map.panTo(this.newCenter(new google.maps.LatLng(obj.lat, obj.lng), -0.25, 0));
  }

  newCenter = (latlng, offsetX, offsetY) =>{
    var span = this.map.getBounds().toSpan();
    return {
        lat: latlng.lat() + span.lat()*offsetY,
        lng: latlng.lng() + span.lat()*offsetX
    };
  }

  setMarkers = () =>{
    const locations = this.props.locations;
    const bounds = new google.maps.LatLngBounds();

    if(this.markers.length){
      for (var i = 0; i < this.markers.length; i++) {
        this.markers[i].setMap(null);
      }
      this.markers = [];
    }

    if(this.infoWindow)
      this.infoWindow.close();
    else
      this.infoWindow = new google.maps.InfoWindow({
          maxWidth: 250
      });

    if(locations.length){
      locations.map((item, key) => {
          var marker = new google.maps.Marker({
              position: new google.maps.LatLng( item.lat, item.lng ),
              animation: google.maps.Animation.DROP,
              title: item.address,
              map: this.map
          });

          bounds.extend(marker.position);
          this.markers.push(marker);
      });

      this.map.fitBounds(bounds);
    }
  }
  render() {
    return (
      <div class="MapContainer"></div>
    );
  }
}
