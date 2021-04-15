//----------------------------------------------------------------------------
// ConfirmMeeting.jsx
// Author: Erin Vuong
// Modal holding stuff for comfirming meeting
//----------------------------------------------------------------------------

import React, { useState } from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import ConfirmForm from './ConfirmForm';

function ConfirmMeeting(props)
{
    const [validated, setValidated] = useState(false);

    const handleSubmit = (event) => {
        const form = event.currentTarget;
        event.preventDefault();
        event.stopPropagation();
        if (form.checkValidity()) {
            props.confirm();
            return; 
        }
        setValidated(true);
    };

    return (
        <Modal show={props.show} onHide={props.hide} size="lg" centered>
            <Modal.Header closeButton>
                <Modal.Title>Confirm meeting</Modal.Title>
            </Modal.Header>
            <Form noValidate validated={validated}
                             className="needs-validation"
                             onSubmit={handleSubmit}>
                <Modal.Body>
                    <p>Almost there! We just need a little more information
                        to confirm your meeting.</p>
                    <ConfirmForm changeName={props.changeName}
                                changeEmail={props.changeEmail}
                                changeNotes={props.changeNotes} />
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary"
                            onClick={props.hide}>
                        Cancel
                    </Button>
                    <Button variant="primary" 
                            type="submit">
                        Schedule Meeting!
                    </Button>
                </Modal.Footer>
            </Form>
        </Modal>
    );
}

export default ConfirmMeeting;
