import React from "react";
import Dimmer from "../components/Dimmer";
import GoogleMap from "../components/GoogleMap";
import Search from "../components/Search";
import LocationsList from "../components/LocationsList";
import MovieDetails from "../components/MovieDetails";
import SearchDetails from "../components/SearchDetails";
import * as ResultsActions from "../actions/ResultsActions";
import ResultsStore from "../stores/ResultsStore";

export default class Layout extends React.Component {
  constructor(props){
    super(props);
    this.state = ResultsStore.getState();
  }

  componentWillMount = () => {
    ResultsStore.on("change", () => {
      this.setState(ResultsStore.getState());
    });
  }

  showResults = (id) =>{
    ResultsActions.loadResultsData(id);
  }

  panToPin = (obj) =>{
    this.refs.map.panToPin(obj);
  }

  render() {
    return (
      <div>
        <Dimmer />
        <Search showResults={this.showResults} />
        {
          this.state.isResultsVisible &&
          <div>
            <section class="SearchResults">
              <MovieDetails data={ this.state.movies } />
              <SearchDetails locationCount={ this.state.locations.length } movieTitle={ this.state.movies.title } city="San Francisco" />
              <LocationsList selectedItem={ this.state.selectedListItem } data={ this.state.locations } submit={ this.panToPin } />
            </section>
          </div>
        }
        <GoogleMap ref="map" data={ this.state.map } locations={ this.state.locations }/>
      </div>
    );
  }
}
