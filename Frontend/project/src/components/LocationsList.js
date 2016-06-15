import React from "react";
import { map } from "../globals";

export default class SearchDetails extends React.Component {

  constructor(props){
    super(props);
    this.state = {
      selectedItem: this.props.selectedItem
    }
  }

  componentWillReceiveProps = (nextProps) =>{
    this.setState({
      selectedItem: nextProps.selectedItem
    });
  }

  handleSelect = (item, index) =>{
    this.setState({
      selectedItem: index
    });

    item.index = index;
    this.props.submit(item);
  }

  render(){
    return(
      <div class="Locations">
        <ul>
          {
            this.props.data.map((item, key) => {
                return (
                  <li class={ key == this.state.selectedItem ? "Selected" : null }
                    key={ key }
                    onClick={ this.handleSelect.bind(this, item, key) }>
                    <span class="Thumb">
                      <img src={ map.staticMapUrl + "&center=" +   item.lat + ","+   item.lng + "&key=" + map.key } />
                    </span>
                    <h3 class="StreetName">{ item.address }</h3>
                    <span class="LatLong">
                      Lat: { item.lat },
                      Long: { item.lng }
                    </span>
                    <i class="Icon material-icons">room</i>
                  </li>
                )
            })
          }
        </ul>
      </div>
    );
  }
}
