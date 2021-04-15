//----------------------------------------------------------------------------
// LandingPage.jsx
// Author: Erin Vuong
// Page for when logged out
//----------------------------------------------------------------------------

import React from 'react';

function LandingPage(props)
{
    const description = 'Intelligent scheduling with your preferences' +
            ' and productivity in mind.';
    return (
        <div className="landing-page">
            <h1 className="text-center">
                {description}
            </h1>
        </div>
    );
}

export default LandingPage;
