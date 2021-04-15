//----------------------------------------------------------------------------
// ScheduleSuccess.jsx
// Author: Erin Vuong
// Modal holding stuff for comfirming meeting
//----------------------------------------------------------------------------

import React, { useState } from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

function ScheduleSuccess(props)
{
    return (
        <Modal show={props.show} onHide={props.hide} size="lg" centered>
            <Modal.Header closeButton>
                <Modal.Title>Meeting confirmed!</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <p>Your meeting for <strong>{props.date}</strong> from 
                {' '}<strong>{props.start}</strong> to <strong>{props.end}</strong>
                {' '}has been confirmed. {props.hostName} will 
                contact you about meeting location details. You should receive a confirmation
                email at <strong>{props.email}</strong>. To reschedule or cancel please contact
                {' '}{props.hostName}.</p>
                <p>If you used a Google email address the event has been added
                    tenatively to your calendar.</p>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="primary"
                        onClick={props.hide}>
                    Done
                </Button>
            </Modal.Footer>
        </Modal>
    );
}

export default ScheduleSuccess;
