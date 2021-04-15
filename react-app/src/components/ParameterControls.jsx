//----------------------------------------------------------------------------
// ParameterControls.jsx
// Author: Erin Vuong
// Parameter control components for logged in user
//----------------------------------------------------------------------------
import React from 'react';
import Form from 'react-bootstrap/Form';
import { HoverInfo } from './FormComponents';

function ParameterControls(props)
{
    const weekdayText = "If you only had one meeting to schedule during the " +
        "week, which day would you schedule it on?";
    const hourText = "If you only had one meeting to schedule during " + 
        "the workday, what time would you schedule it to start?";
    return (
        <div className="parameter-controls">
            <div className="text-center">
                <h3>{"Update preferences for " + props.name}</h3>
                <p className="params-text">
                    These preferences are used during scheduling to try and rank
                    your available time slots by preferability. More preferable time
                    slots are then presented first to increase the likelihood they
                    are picked. We automatically prioritize time slots that don't
                    fragment your existing unscheduled time.
                </p>
            </div>
            <Form>
                <Form.Group controlId="paramForm.weekdays">
                    <Form.Label>Preferred scheduling day of the week</Form.Label>
                    <HoverInfo id="pref-weekdays" tooltipText={weekdayText} />
                    <Form.Control as="select"
                                    value={props.weekday}
                                    onChange={props.changeDay}>
                        <option value="0">Monday</option>
                        <option value="1">Tuesday</option>
                        <option value="2">Wednesday</option>
                        <option value="3">Thursday</option>
                        <option value="4">Friday</option>
                        <option value="5">Saturday</option>
                        <option value="6">Sunday</option>
                    </Form.Control>
                </Form.Group>
                <Form.Group controlId="paramForm.hour">
                    <Form.Label>Preferred scheduling hour of the day</Form.Label>
                    <HoverInfo id="pref-hour" tooltipText={hourText} />
                    <Form.Control type="time"
                                    value={props.hour}
                                    onChange={props.changeHour}>
                    </Form.Control>
                </Form.Group>
            </Form>
        </div>
    );
}

export default ParameterControls;
