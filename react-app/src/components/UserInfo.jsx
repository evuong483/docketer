//----------------------------------------------------------------------------
// UserInfo.jsx
// Author: Erin Vuong
// User info display
//----------------------------------------------------------------------------
import React from 'react';
import Form from 'react-bootstrap/Form';

function UserInfo(props)
{
    const greeting = "Hello, " + props.name.split(" ")[0] + "!";
    return (
            <div className="user-info"> 
                <h1>{greeting}</h1>
                <Form>
                    <Form.Group>
                        <Form.Label>Your email is</Form.Label>
                        <Form.Control type="text"
                                      placeholder={props.email} readOnly />
                    </Form.Group>
                </Form>
            </div>
    );
}

export default UserInfo;
