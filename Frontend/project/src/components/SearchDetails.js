import React from "react";

export default class SearchDetails extends React.Component {
  render(){
    return(
      <div class="SearchDetails">
        <span>
          Found
          <span class="Count">{ this.props.locationCount }</span>
          locations in { this.props.city } , where
          <br/>
          "{ this.props.movieTitle }"
          <br/>
          have been filmed.
        </span>
      </div>
    );
  }
}
