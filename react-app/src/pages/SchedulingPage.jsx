//----------------------------------------------------------------------------
// SchedulingPage.jsx
// Author: Erin Vuong
// Page for scheduling meetings
//----------------------------------------------------------------------------

import React, { useEffect, useState } from 'react';
import ScheduleGreeting from '../components/ScheduleGreeting';
import Loading from '../components/Loading';
import Scheduler from '../components/Scheduler';
import { fetchData } from '../helper';

function SchedulingPage(props)
{
    const [name, setName] = useState("");
    const [email, setEmail] = useState(""); // not being used
    const [times, setTimes] = useState([]);
    const [fetched, setFetched] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        fetchData('/fetch_user', 
                    { target: props.target },
                    'Fetch user error',
                    (data) => {
                        if ('error' in data) {
                            setError(data.error);
                            return;
                        }
                        setName(data.name);
                        setEmail(data.email);
                    });
        fetchData('/fetch_times',
                    { target: props.target },
                    'Fetch times error',
                    (data) => {
                        if ('error' in data) {
                            setError(data.error);
                            return;
                        }
                        setTimes(data);
                        setFetched(true);
                     });
    }, []);

    return (
        <div className="scheduling-page text-center">
            { name &&
                <ScheduleGreeting name={name} />
            }
            { error &&
                <p>{ error }</p>
            }
            { fetched && !error
                ? <Scheduler times={times}  target={props.target} name={name} error={setError} />
                : !error && <Loading caption="Fetching available times" />
            }
        </div>
    );
}

export default SchedulingPage;
