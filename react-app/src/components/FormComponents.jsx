//----------------------------------------------------------------------------
// FormComponents.jsx
// Author: Erin Vuong
// Form components for link generator
//----------------------------------------------------------------------------

import React from 'react';
import Form from 'react-bootstrap/Form';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faInfoCircle } from '@fortawesome/free-solid-svg-icons';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';

function HoverInfo(props) 
{
    return (
        <OverlayTrigger key={props.id + "-info"}
                        placement="right"
                        overlay={
                            <Tooltip id={props.id+"-tooltip"}>
                                {props.tooltipText}
                            </Tooltip>
                        }>
            <FontAwesomeIcon icon={faInfoCircle}
                             className="text-info info-icon"/>
        </OverlayTrigger>
    );
}

// props: id, label (display label), info (tooltip text)
function LabelAndInfo(props)
{
    return (
        <>
        <Form.Label htmlFor={props.id}>
                    {props.label} 
        </Form.Label>
        <HoverInfo key={props.id}
                           placement="right"
                           id={props.id}
                           tooltipText={props.info} />
        </>
    );
}

function GeneralFormGroup(props) 
{
    return (
       <Form.Group>
            <LabelAndInfo id={props.controlId}
                          label={props.label}
                          info={props.info} />
            <Form.Control {...props} />
            {props.feedback &&
                <Form.Control.Feedback {...props.feedback}>
                    {props.feedback.text}
                </Form.Control.Feedback>
            }
        </Form.Group>
        );

}

function Checked(props)
{
    return (
        <Form.Group className="checked">
            <Form.Label>
                {props.label}
            </Form.Label>
            <HoverInfo key={props.id + "-info"}
                    placement="right"
                    id={props.id + "-tooltip"}
                    tooltipText={props.info} /> {' '}
            <Form.Check inline type='checkbox'
                            id={props.id}
                            checked={props.checked}
                            onChange={props.toggle} />
        </Form.Group>
    );
}

function DaySelector(props)
{
    
    const weekInfo = "On which days can this meeting be scheduled?";
    return (
        
        <Form.Group className="weekday-selector">
            <Form.Label>
                Workweek days
            </Form.Label>
            <HoverInfo key={"weekday-selector-info"}
                        placement="right"
                        id={"weekday-selector-tooltip"}
                        tooltipText={weekInfo} />
            <br />
            {props.weekdays.map((day, index) => (
                <Form.Check inline label={day}
                                    type="checkbox"
                                    id={"day-" + ((index + 6) % 7)}
                                    checked={props.checked[index]}
                        onChange={() => props.toggleCheckbox(index)}/>
            ))}
        </Form.Group>
        
    );
}

export { GeneralFormGroup, DaySelector, LabelAndInfo, HoverInfo, Checked };
