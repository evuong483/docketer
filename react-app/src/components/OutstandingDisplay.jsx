//----------------------------------------------------------------------------
// OutstandingDisplay.jsx
// Author: Erin Vuong
// Display list for outstanding links
//----------------------------------------------------------------------------

import React, { useState, useEffect } from 'react';
import Jumbotron from 'react-bootstrap/Jumbotron';
import ListGroup from 'react-bootstrap/ListGroup';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons';
import { faCopy } from '@fortawesome/free-regular-svg-icons';
import { Badge, OverlayTrigger, Tooltip } from 'react-bootstrap';

function IconLink(props)
{   
    return (
        <a onClick={ props.onClick }
           onMouseOut={ props.onMouseOut }>
                <OverlayTrigger key={props.id}
                                placement="top"
                                overlay={
                                    <Tooltip id={props.id + "-tooltip"}>
                                        {props.tooltip}
                                    </Tooltip>
                                } >
                    <FontAwesomeIcon icon={props.icon} />
                </OverlayTrigger>
        </a>
    );
}

function OutstandingDisplay(props)
{
    const [linkList, setLinkList] = useState([]);
    const [tooltipCopy, setTooltipCopy] = useState('Copy');

    useEffect(() => {
        setLinkList(props.links.map((x, i) => {
            const url = window.location.origin + "/schedule/" + x.target;
            return (
                <ListGroup.Item>
                    { url + '  '}
                    { !x.deleted ? 
                        <>
                        <IconLink onClick={() => {
                                    navigator.clipboard.writeText(url);
                                    setTooltipCopy('Copied!')}}
                                onMouseOut={() => {setTooltipCopy('Copy')}}
                                id={x.target + '-copy'}
                                icon={ faCopy }
                                tooltip={tooltipCopy} />{' '}
                        <IconLink onClick={() => {props.delete(i)}}
                                id={x.target + '-delete'}
                                icon={faTimes}
                                tooltip="Delete" /> {' '}
                        </>     
                        :
                        <Badge variant="danger">Deleted</Badge>
                    }
                    { x.new && !x.deleted &&
                        <Badge variant="success">New</Badge>
                    }
                </ListGroup.Item>
            );
        }));
    }, [props.links, tooltipCopy]);

    return (
        <Jumbotron className="outstanding-display">
            <h2>Here are your oustanding scheduling links.</h2>
            <p>
                You can copy or delete links here.
            </p>
            <p>
                <strong>Note that if you delete a link it can no longer be used for scheduling.</strong>
            </p>
            <p>
                Links will be deleted automatically once they have been used.
            </p>
            <ListGroup>
                {linkList}
            </ListGroup>
        </Jumbotron>
    );
}

export default OutstandingDisplay;
export { IconLink };