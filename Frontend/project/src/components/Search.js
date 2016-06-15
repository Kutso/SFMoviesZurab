import React from "react";
import AutocompleteList from "../components/AutoComplete";
import * as SearchActions from "../actions/SearchActions";

import SearchStore from "../stores/searchstore";

export default class Search extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      searchValue: "",
      isLoading: SearchStore.getState().isLoading,
      searchResults: SearchStore.getState().searchResults
    }
  }

  componentWillMount =()=>{
    SearchStore.on("change", () => {
      this.setState({
        isLoading: SearchStore.getState().isLoading,
        searchResults: SearchStore.getState().searchResults
      });
    })
  }

  handleInput = (event) => {
    const searchValue = event.target.value;
    this.setState({ searchValue });
    if(searchValue)
      SearchActions.loadSearchData(searchValue);
    else
      this.handleClear();
  }

  handleClear = (event) => {
    if(this.state.searchValue.length){
      SearchActions.clearSearch();
      this.setState({ searchValue: "" });

      //Focus search input
      document.getElementById("searchInput").focus();
    }
  }

  submit = (obj) =>{
    this.setState({
      searchValue: obj.title,
      searchResults: []
    });
    this.props.showResults(obj.id);
  }

  render(){
    return(
      <div class="SearchInput">
        <span class="Input">
          <i class="Icon Search material-icons">search</i>
          {
            this.state.searchValue.length && !this.state.isLoading ?
            <i onClick={ this.handleClear } class="Icon Clear Active material-icons" title="Clear">clear</i> :
            this.state.isLoading ? <i class="Icon Spinner material-icons">autorenew</i> : null
          }

          <input id="searchInput" type="text" placeholder="Find Movies (e.g. Need For Speed)" autoComplete="off" autoFocus
            value={ this.state.searchValue }
            onChange={ this.handleInput }
          />

        </span>

        { this.state.searchResults.length ? <AutocompleteList submit={ this.submit } data={ this.state.searchResults } /> : null }
      </div>
    );
  }
}
