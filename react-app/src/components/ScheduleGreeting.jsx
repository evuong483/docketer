//----------------------------------------------------------------------------
// ScheduleGreeting.jsx
// Author: Erin Vuong
// Greeting for scheduling page
//----------------------------------------------------------------------------
import React from 'react';

function ScheduleGreeting(props)
{
    return (
        <h2 className="text-center">
                {`Scheduling with ${props.name}`}
        </h2> 
     
    );
}

export default ScheduleGreeting;