import { EventEmitter } from "events";
import dispatcher from "../dispatcher";

class SearchStore extends EventEmitter {
    constructor(props) {
        super(props);
        this.state = {
            searchResults: [],
            isLoading: false
        };
    }

    fetchSearch = () =>{
        this.state.isLoading = true;
        this.emit("change");
    }

    recieveSearch = (data) => {
        this.state.searchResults = data;
        this.state.isLoading = false;
        this.emit("change");
    }

    clearSearch = () =>{
        this.state = {
            searchResults: [],
            isLoading: false
        };
        this.emit("change");
    }

    getState(){
        return this.state;
    }

    handleActions = (action) =>{
        switch (action.type) {
            case "FETCH_SEARCH_DATA":
                this.fetchSearch();
                break;
            case "RECEIVE_SEARCH_DATA":
                this.recieveSearch(action.data);
                break;
            case "CLEAR_SEARCH":
                this.clearSearch();
                break;
        }
    }
}

const searchStore = new SearchStore;
dispatcher.register(searchStore.handleActions);
export default searchStore;
