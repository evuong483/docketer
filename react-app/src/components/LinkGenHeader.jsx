//----------------------------------------------------------------------------
// LinkGenHeader.jsx
// Author: Erin Vuong
// Form for generating one-time scheduling link
//----------------------------------------------------------------------------
import React from 'react';

function LinkGenHeader(props)
{
    return (
        <div className="text-center">
            <h2>Generate a one-time scheduling link</h2>
            <p>
                A meeting can be scheduled up to {props.weeksOut} weeks in advance.{' '}
                <a href="#" onClick={props.toggleVisibility}>
                    { props.visible
                        ? "Hide advanced options."
                        : "Show advanced options."
                    }
                </a> 
            </p>
        </div>
    );
}

export default LinkGenHeader;