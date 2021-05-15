import ID3 from "./ID3"
import { BrowserRouter as Router, Route, Link } from "react-router-dom";


import './App.css';

import aladin from "./assets/images/Aladin.png"

function App() {
	return (
		<Router>
			<div className="app">
						
				<div className="app__image">
					<img alt="aladín" src={aladin} />
				</div>

				<div className="app_id3">
					<Route path="/" exact component={ID3} />
				</div>

			</div>
    	</Router>
	);
}

export default App;
