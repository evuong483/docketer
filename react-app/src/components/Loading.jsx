//----------------------------------------------------------------------------
// Loading.jsx
// Author: Erin Vuong
// Loading component
//----------------------------------------------------------------------------
import React from 'react';
import Spinner from 'react-bootstrap/Spinner';

function Loading(props)
{
    return (
        <div className="loading">
            <p>{props.caption + "..."}</p>
            <Spinner animation="border" />
        </div>
    );
}

export default Loading;