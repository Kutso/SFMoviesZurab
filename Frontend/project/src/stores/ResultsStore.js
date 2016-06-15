import { EventEmitter } from "events";
import dispatcher from "../dispatcher";

class ResultsStore extends EventEmitter {
    constructor(props) {
        super(props);
        this.state = {
            isResultsVisible: false,
            movies: [],
            locations: [],
            map:{
                center:{
                    lat: 37.7806041,
                    lng: -122.479205
                }
            },
            selectedListItem: null
        };
    }

    clearSearch = () =>{
        this.state = {
            isResultsVisible: false,
            movies: [],
            locations: [],
            selectedListItem: null
        };
        this.emit("change");
    }

    showResults = (data) =>{
        this.state = {
            isResultsVisible: true,
            movies: data.movie_data,
            locations: data.locations,
            selectedListItem: null
        };
        this.emit("change");
    }

    getState(){
        return this.state;
    }

    handleActions = (action) =>{
        switch (action.type) {
            case "CLEAR_SEARCH":
                this.clearSearch();
                break;
        }
        switch (action.type) {
            case "RECEIVE_RESULTS_DATA":
                this.showResults(action.data);
                break;
        }
        switch (action.type) {
            case "FETCH_RESULTS_DATA":
                //this.fetchResults();
                break;
        }
    }
}

const resultsStore = new ResultsStore;
dispatcher.register(resultsStore.handleActions);
export default resultsStore;
