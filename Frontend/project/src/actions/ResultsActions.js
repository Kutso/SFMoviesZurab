import dispatcher from "../dispatcher";
import { app } from "../globals";
import axios from "axios";

export function loadResultsData(id){
  dispatcher.dispatch({ type: "FETCH_RESULTS_DATA" });

  axios.get(app.api + "movies/" + id + "/")
    .then(function (response) {
      dispatcher.dispatch({  type: "RECEIVE_RESULTS_DATA", data: response.data });
    })
    .catch(function (response) {
      console.log("Catch RECEIVE_RESULTS_DATA response", response);
    });
}
