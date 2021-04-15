//----------------------------------------------------------------------------
// LoggedIn.jsx
// Author: Erin Vuong
// Page for when logged out
//----------------------------------------------------------------------------

import React, { useState, useEffect } from 'react';
import Alert from 'react-bootstrap/Alert';
import ParameterControls from '../components/ParameterControls';
import UserInfo from '../components/UserInfo';
import LinkGenerator from '../components/LinkGenerator';
import { fetchData } from '../helper';
import OutstandingDisplay from '../components/OutstandingDisplay';

function LoggedIn(props)
{
    const [name , setName] = useState("");
    const [email, setEmail] = useState("");
    const [hour, setHour] = useState("10:00");
    const [day, setDay] = useState("2");
    const [links, setLinks] = useState([]);

    useEffect(() => {
        // get info from backend
        fetchData('/user_info', {}, 'Fetch user error',
                  (data) => {
                        setName(data.name);
                        setEmail(data.email);
                        setHour(data.optimal_hour);
                        setDay(data.optimal_day);
                        setLinks(data.links);
                  });
    }, []);

    const deleteLink = (index) => {
        fetchData('/delete_link', 
                  {target: links[index].target},
                  'Delete link error',
                  () => {return});
        const newArray = JSON.parse(JSON.stringify(links));
        newArray[index].deleted = true;
        setLinks(newArray);
    };

    const addLink = (ext) => {
        const newArray = JSON.parse(JSON.stringify(links));
        newArray.unshift({target: ext, new: true});
        setLinks(newArray);
    };

    const changeHour = (event) => {
        fetchData('/change_hour',
                  {hour: event.target.value},
                  'Change hour error',
                  (data) => { console.log(data) } );
        setHour(event.target.value);
    }

    const changeDay = (event) => {
        fetchData('/change_day',
                  {weekday: event.target.value},
                  'Change day error',
                  (data) => { console.log(data) } );
        setDay(event.target.value);
    }

    return (
        <div className="user-page">
            { props.error &&
                <Alert key="error" variant='danger'>
                    There is an issue with the connection to your Google account.
                    Please click <Alert.Link href="/logout_force">this link </Alert.Link> 
                    {' '}to fix this.
                </Alert>
            }
            { name &&
                <UserInfo name={name} email={email} />
            }
            <LinkGenerator addLink={addLink} />
            <ParameterControls name={name}
                               weekday={day}
                               hour={hour}
                               changeDay={changeDay}
                               hangeHour={changeHour}/>
            { links.length > 0 &&
                <OutstandingDisplay links={links}
                                    delete={deleteLink} />
            }
        </div>
    );
}

export default LoggedIn;
