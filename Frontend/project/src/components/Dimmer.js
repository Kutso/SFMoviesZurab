import React from "react";

export default class Dimmer extends React.Component {
  constructor(props){
    super(props);

    this.state = {
      isVisible: localStorage.isDimmerHidden || 1
    }
  }

  handleHide = (event) =>{
    event.preventDefault();
    localStorage.isDimmerHidden = 0;
    this.setState({
        isVisible: localStorage.isDimmerHidden
    });

    //Focus search input
    document.getElementById("searchInput").focus();
  }

  handleShow = () =>{
    localStorage.isDimmerHidden = 1;
    this.setState({
        isVisible: localStorage.isDimmerHidden
    });
  }

  render(){
    if(Number(this.state.isVisible))
      return(
        <div class="Dimmer" onClick={ this.handleHide }>
          <div class="Info">
            <span class="Logo"></span>
            <p>Service that shows on a map where movies have been filmed in San Francisco.</p>
            <a href="#">Got it</a>
          </div>
        </div>
      )
    else
      return(
        <i onClick={ this.handleShow } class="InfoDimmer material-icons">help</i>
      )
  }
}
