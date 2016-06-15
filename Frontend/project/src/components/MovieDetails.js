import React from "react";

export default class MovieDetails extends React.Component {
  constructor(props){
    super(props);
  }

  render(){
    return(
      <div class={ this.props.data.poster_url ? "MovieDetails" : "MovieDetails NoPoster" } style={
          this.props.data.poster_url && {
            backgroundImage: "url(" + this.props.data.poster_url + ")"
          }
        }>
        <div class="Details">
          <h2 class="Title">{ this.props.data.title }</h2>
          <span class="InfoItem">
            <strong>Director:</strong>
            <span>{ this.props.data.director }</span>
          </span>
          { this.props.data.imdb_rating && <i class="Rating">{ this.props.data.imdb_rating }</i> }
        </div>
      </div>
    );
  }
}
