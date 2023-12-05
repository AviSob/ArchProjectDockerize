import logo from './logo.png';
import './App.css';

import EndpointAudit from './components/EndpointAudit'
import AppStats from './components/AppStats'
import HealthStats from './components/HealthStats'

function App() {

    const endpoints = ["movies/movie_ratings", "movies/movie_saved"]

    const rendered_endpoints = endpoints.map((endpoint) => {
        return <EndpointAudit key={endpoint} endpoint={endpoint}/>
    })

    return (
        <div className="App">
            <img src={logo} className="App-logo" alt="logo" />
            <div>
                <h1>Latest Stats</h1>
                <AppStats/>
                <br></br>
            </div>
            <div>
                <h1>Audit Endpoints</h1>
                {rendered_endpoints}
                <br></br>
            </div>
            <div>
                <h1>Service Health Stats</h1>
                <HealthStats/>
                <br></br>
            </div>
        </div>
    );

}



export default App;
