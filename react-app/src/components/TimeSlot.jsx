//----------------------------------------------------------------------------
// TimeSlot.jsx
// Author: Erin Vuong
// Button representing a time slot
//----------------------------------------------------------------------------
import React from 'react';
import Button from 'react-bootstrap/Button';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faClock } from '@fortawesome/free-regular-svg-icons';

function TimeSlot(props) 
{
    return (
        <div className="time-slot-button">
            <Button variant="outline-secondary"
                    size="lg"
                    className="carousel-button"
                    onClick={props.onClick}>
                 <p>{props.date}</p>
                 <FontAwesomeIcon icon={faClock} />
                 <h3>{props.start} to {props.end}</h3>{"\n"}
                 Yes, this time works for me.
            </Button>
        </div>
    );
}

export default TimeSlot;