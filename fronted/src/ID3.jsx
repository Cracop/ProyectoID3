import { Component } from "react";

import "./assets/styles/id3.css";

class ID3 extends Component {
    state = {
        pregunta: "Tu personaje es Guapo?",
        respuesta_1: "Bruno Lo es",
        respuesta_2: "El Rodrigo se la come",
    }

    handleClick = (e) => {
        console.log("HI");
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
                        value={this.state.respuesta_1}
                    >
                        {this.state.respuesta_1}
                    </button>
                </div>
                <div className="item respuesta_2">
                    <button 
                        className="btn_respuesta_2"
                        onClick={this.handleClick}
                        value={this.state.respuesta_2}
                    >
                        {this.state.respuesta_2}
                    </button>
                </div>
            </div>

        )
    }
}

export default ID3;