import React from "react";

export default class Autocomplete extends React.Component {
  render(){
    return(
      <ul class="Autocomplete">
        {
          this.props.data.map((item, key) => {
            return (
              <li key={ item.id } onClick={ this.props.submit.bind(this, item) }>
                <i class="Icon material-icons">movie</i>
                <span class="Title">{ item.title }</span>
                <span class="SubTitle">{ item.year }</span>
              </li>
            )
          })
        }
      </ul>
    );
  }
}
