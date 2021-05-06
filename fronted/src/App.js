import ID3 from "./ID3"

import './App.css';

import aladin from "./assets/images/Aladin.png"

function App() {
	return (
		<div className="app">
					
			<div className="app__image">
				<img alt="aladín" src={aladin} />
			</div>

			<div className="app_id3">
				<ID3 />
			</div>

		</div>
	);
}

export default App;
