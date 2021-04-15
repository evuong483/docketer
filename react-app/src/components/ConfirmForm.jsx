//----------------------------------------------------------------------------
// ConfirmForm.jsx
// Author: Erin Vuong
// Form used to gather user info and schedule meeting
//----------------------------------------------------------------------------

import React from 'react';
import { GeneralFormGroup } from './FormComponents';

function ConfirmForm(props)
{
    var nameInfo = "Please provide your name (first and last is preferred).";
    var emailInfo = "This will be used to send you meeting details. " +
                    "We'll never share your email with anyone else.";
    var noteInfo = "Anything you want to share with the meeting host."
    return (
        <>
            <GeneralFormGroup controlId="name"
                              label="Name"
                              type="text"
                              onChange={(event) => {props.changeName(event.target.value)}}
                              placeholder="Name"
                              info={nameInfo}
                              feedback={{
                                  text: "Please provide a name.",
                                  type: "invalid"
                              }}
                              required={true} />
            <GeneralFormGroup controlId="email"
                              label="Email address"
                              type="email"
                              onChange={(event) => {props.changeEmail(event.target.value)}}
                              info={emailInfo}
                              placeholder="email@example.com"
                              feedback={{
                                text: "Please provide a valid email address.",
                                type: "invalid"
                              }}                              
                              required={true} />
            <GeneralFormGroup controlId="notes"
                              label="Additional notes"
                              as="textarea"
                              info={noteInfo}
                              onChange={(event) => {props.changeNotes(event.target.value)}}
                              placeholder="Optional notes for the host..." />
        </>
    );
}

export default ConfirmForm;
