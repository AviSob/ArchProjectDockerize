import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://avi.northcentralus.cloudapp.azure.com/healthcheck/status`)
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
                <div className='sectionsContainer'>
                    <div className='section'>
                        <p><b>Receiver:</b></p> {stats['receiver']}
                    </div>
                    <div className='section'>
                        <p><b>Storage:</b></p> {stats['storage']}                         
                    </div>
                    <div className='section'>
                        <p><b>Processing:</b></p> {stats['processing']}                         
                    </div>
                    <div className='section'>
                        <p><b>Audit:</b></p> {stats['audit']}                         
                    </div>
                </div>
                <h3>Last Updated: {stats['last_updated']}</h3>

            </div>
        )
    }
}
