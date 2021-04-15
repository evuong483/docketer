//----------------------------------------------------------------------------
// Client.js
// Author: Erin Vuong
// Base for internal stuff
//----------------------------------------------------------------------------

import React, { useState } from 'react';
import Header from './components/Header';
import LandingPage from './pages/LandingPage';
import LoggedIn from './pages/LoggedIn';
import Footer from './components/Footer';

function Client()
{
    const [isLoggedIn, setLoggedIn] = useState(window.loggedIn === 'T');
    const [error, setError] = useState(window.error === 'T');
    const loggedInUrl = 'https://docs.google.com/document/d/1uFg-jsFCzDis5LvxQ1Kj1aIRS7ndyUPSUJRlZSwnoBI/edit?usp=sharing';

    const toggle = () => {
        if (isLoggedIn) {
            window.location.href = window.location.origin + '/logout';
        } else {
            window.location.href = window.location.origin + '/login';
        }
    }

    return (
        <>
            <Header toggle={toggle}
                    isLoggedIn={isLoggedIn}
                    showLogin={true} />
            { isLoggedIn
                ? <LoggedIn error={error} />
                : <LandingPage />
            }
            <Footer url={loggedInUrl} />
        </>
    );
}

export default Client;
