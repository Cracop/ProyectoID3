import axios from 'axios';
const URL = 'http://localhost:8000/id3';

export default class Connection{

    constructor(){}


    getStart() {
        const url = `${URL}/`;
        return axios.get(url).then(response => response.data);
    }

    ans( answer ) {
        const url = `${URL}/${answer}/`
        return axios.get(url).then(response => response.data)
    }


}