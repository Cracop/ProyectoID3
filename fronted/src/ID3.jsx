import { Component } from "react";

import "./assets/styles/id3.css";
import Connection from "./Connection";

const connection = new Connection()

class ID3 extends Component {
    state = {
        pregunta: "En espera",
        respuesta_1: "Verdadero",
        respuesta_2: "Falso",
    }


    componentDidMount() {
        connection.getStart().then((result) => {
            console.log(result)
            this.setState({
                ...this.state,
                pregunta: "¿" + result.pregunta + "?"
            })
        })
    }   

    handleClick = (e) => {
        const ans = e.target.value;
        connection.ans(ans).then((result) => {
            console.log(result)
            if(result.status === "Diagnostico Final"){
                this.setState({
                    ...this.state,
                    pregunta: result.status + ": " + result.pregunta,
                })
            } else {
                this.setState({
                    ...this.state,
                    pregunta: "¿" + result.pregunta + "?"
                })
            }
        })
    }

    render(){
        return(

            <div className="id3">
                <div className="item pregunta">
                    {this.state.pregunta}
                </div>
                <div className="item respuesta_1">
                    <button 
                        className="btn_respuesta_1" 
                        onClick={this.handleClick}
                        value="1"
                    >
                        {this.state.respuesta_1}
                    </button>
                </div>
                <div className="item respuesta_2">
                    <button 
                        className="btn_respuesta_2"
                        onClick={this.handleClick}
                        value="0"
                    >
                        {this.state.respuesta_2}
                    </button>
                </div>
            </div>

        )
    }
}

export default ID3;