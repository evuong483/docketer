//----------------------------------------------------------------------------
// OutOfTime.jsx
// Author: Erin Vuong
// Page that shows when the user runs out of available times
//----------------------------------------------------------------------------

import React from 'react';

function OutOfTime(props)
{
    return (
        <p className="text-center">
            It looks like there are no available times that work for you.
            Please contact {props.hostName} to schedule your meeting.
        </p>
    );
}

export default OutOfTime;