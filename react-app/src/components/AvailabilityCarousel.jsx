//----------------------------------------------------------------------------
// AvailabilitySelector.jsx
// Author: Erin Vuong
// Availability selection carousel component
//----------------------------------------------------------------------------

import React, { useState, useEffect } from 'react';

import Button from 'react-bootstrap/Button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUndoAlt, faTimes } from '@fortawesome/free-solid-svg-icons';

import TimeSlot from './TimeSlot';
import OutOfTime from './OutOfTime';

function AvailabilityCarousel(props) 
{
    const [showIndex, setIndex] = useState(0);
    const [times, setTimes] = useState([]);

    useEffect(() => {
        setTimes(props.times.map((slot, index) => {
            return (
                <>
                <p className="text-center">
                    Does this time work for you?
                </p>
                <TimeSlot date={slot.pretty_date}
                          start={slot.start}
                          end={slot.end}
                          onClick={() => {
                              props.updateInfo(slot.start, slot.end,
                                               slot.buffer, slot.date,
                                               slot.pretty_date);
                              props.showConfirm();
                          }} />
                <Button size="sm"
                        variant="outline-danger"
                        onClick={() => { setIndex(index + 1) }}
                        className="carousel-button">
                    <FontAwesomeIcon icon={faTimes} />
                    {' '}No, show me another time.
                </Button>
                </>
            );
    }))}, []);    
    console.log("Length " + times.length);    

    return (
        <>
        {showIndex < times.length 
            ? times[showIndex]
            : <>
                <OutOfTime hostName={props.name} />
                <Button size="sm"
                        variant="outline-warning"
                        onClick={() => { setIndex(0) }}
                        className="carousel-button">
                    <FontAwesomeIcon icon={faUndoAlt} />
                    {' '}Show me the times again.
                </Button>
            </>
        }
        </>
    );
}

export default AvailabilityCarousel;