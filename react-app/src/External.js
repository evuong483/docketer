//----------------------------------------------------------------------------
// External.js
// Author: Erin Vuong
// Base for external stuff
//----------------------------------------------------------------------------

import React from 'react';
import Footer from './components/Footer';
import Header from './components/Header';
import SchedulingPage from './pages/SchedulingPage';

function External(props)
{
    const scheduleUrl = "https://docs.google.com/document/d/1FZGoeQps5YBUeevAp_zUig0guIGgJjFvd-dx14NKvZY/edit?usp=sharing";

    return (
        <>
            <Header showLogin={false} />
            <SchedulingPage target={props.match.params.target} />
            <Footer url={scheduleUrl} />
        </>
    );
}

export default External;
