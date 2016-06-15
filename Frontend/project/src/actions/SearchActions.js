import dispatcher from "../dispatcher";
import { app } from "../globals";
import axios from "axios";

export function clearSearch(){
  dispatcher.dispatch({ type: "CLEAR_SEARCH" });
}

export function loadSearchData(searchValue){
  dispatcher.dispatch({ type: "FETCH_SEARCH_DATA" });

  axios.get(app.api + "movies/autocomplete/" + searchValue + "/")
    .then(function (response) {
      dispatcher.dispatch({  type: "RECEIVE_SEARCH_DATA", data: response.data });
    })
    .catch(function (response) {
      dispatcher.dispatch({  type: "RECEIVE_SEARCH_ERROR", data: response });
    });
}
