import logo from './logo.png';
import './App.css';

import EndpointAudit from './components/EndpointAudit'
import AppStats from './components/AppStats'

function App() {

    const endpoints = ["movies/movie_ratings", "movies/movie_saved"]

    const rendered_endpoints = endpoints.map((endpoint) => {
        return <EndpointAudit key={endpoint} endpoint={endpoint}/>
    })

    return (
        <div className="App">
            <img src={logo} className="App-logo" alt="logo" />
            <div>
                <AppStats/>
                <br></br>
            </div>
            <div>
                <h1>Audit Endpoints</h1>
                {rendered_endpoints}
            </div>
        </div>
    );

}



export default App;
