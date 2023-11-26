import React, { useEffect, useState, useCallback } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
        fetch(`http://avi.northcentralus.cloudapp.azure.com/processing/movies/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
  
      useEffect(() => {
        getStats();
      }, [getStats]);
      
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div className='all'>
                <h1>Latest Stats</h1>
                <div className='sectionsContainer'>
                    <div className='section'>
                        <p><b>total number of rated movies:</b></p> {stats['num_rate_readings']}
                    </div>
                    <div className='section'>
                        <p><b>total number of saved movies:</b></p> {stats['num_saves_readings']}                         
                    </div>
                    <div className='section'>
                        <p><b>Most active user:</b></p> {stats['most_active_user']}                         
                    </div>
                    <div className='section'>
                        <p><b>highest rating by:</b></p> {stats['highest_rated']}                         
                    </div>
                </div>
                <h3>Last Updated: {stats['last_updated']}</h3>

            </div>
        )
    }
}
