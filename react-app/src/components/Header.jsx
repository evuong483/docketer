//----------------------------------------------------------------------------
// Header.jsx
// Author: Erin Vuong
// Header component
//----------------------------------------------------------------------------

import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';

function Header(props)
{
    return (
        <Navbar bg="light" variant="light">
            <Navbar.Brand>
                <img
                    src={process.env.PUBLIC_URL + "/images/favicon.ico"}
                    width="30"
                    height="30"
                    className="d-inline-block align-top"
                    alt="Clock Favicon"
                />{' '}
                Docketer
            </Navbar.Brand> 
            {props.showLogin &&
                <Nav.Item className="ml-auto">
                    <Button variant="outline-primary"
                            id="login-button"
                            onClick={() => props.toggle()}>
                        {props.isLoggedIn ? 'Logout' : 'Login'}
                    </Button>
                </Nav.Item>
            }
        </Navbar>
    );
}

export default Header;
