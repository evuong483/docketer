//----------------------------------------------------------------------------
// LinkDisplay.jsx
// Author: Erin Vuong
// Displays generated scheduling link
//----------------------------------------------------------------------------
import React, { useState } from 'react';
import Row from 'react-bootstrap/Row';
import Form from 'react-bootstrap/Form';
import { faCopy } from '@fortawesome/free-regular-svg-icons';
import Spinner from 'react-bootstrap/Spinner';
import { IconLink } from './OutstandingDisplay';

function LinkDisplay(props)
{
    const [tooltip, setTooltip] = useState('Copy')
    return (
        <>
        { props.link && props.link != 'loading' &&
            <Row>
                <Form.Group>
                    <Form.Label className="link-label" >
                        Share this one-time scheduling link to
                        schedule a meeting!{' '}
                        <IconLink onClick={() => {
                                navigator.clipboard.writeText(props.link);
                                setTooltip('Copied!')}}
                              onMouseOut={() => {setTooltip('Copy')}}
                              id={'generated-copy'}
                              icon={ faCopy }
                              tooltip={tooltip} />
                    </Form.Label>
                    <Form.Control type="text"
                                  className="link-display"
                                  value={props.link}
                                  readOnly />
                    <Form.Text className="text-muted" >
                        Once the meeting is booked you will receive
                        an email with details and it will be
                        added to your integrated calendar.
                    </Form.Text>
                </Form.Group>
            </Row>
        }
        {
            props.link === 'loading' &&
            <div className='text-center link-label'>
                <Spinner animation='border'/>
            </div>
        }
        </>
    );
}

export default LinkDisplay;