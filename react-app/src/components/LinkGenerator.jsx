//----------------------------------------------------------------------------
// LinkGenerator.jsx
// Author: Erin Vuong
// Form for generating one-time scheduling link
//----------------------------------------------------------------------------
import React, { useState } from 'react';

import Form from 'react-bootstrap/Form';
import Jumbotron from 'react-bootstrap/Jumbotron';
import { Row, Col } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';

import { GeneralFormGroup, DaySelector, Checked } from './FormComponents';
import { fetchData } from '../helper';
import LinkDisplay from './LinkDisplay';
import LinkGenHeader from './LinkGenHeader';

function LinkGenerator(props)
{
    const [meetingLen, setLen] = useState('60');
    const [buffer, setBuffer] = useState('10');
    const [workdayStart, setWorkdayStart] = useState('09:00');
    const [workdayEnd, setWorkdayEnd] = useState('17:00');
    const [optionsVisible, setVisibile] = useState(false);
    const [weekdays, setWeekdays] = useState(
                            ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 
                                'Thursday', 'Friday', 'Saturday']);
    const [checked, setChecked] = useState(
                                    [false, true, true, true, true, true, false]);
    const [daysOut, setDaysOut] = useState('1');
    const [weeksOut, setWeeksOut] = useState('4');
    const [link, setLink] = useState('');
    const [halfHours, setHalfHours] = useState(true);

    const toggleVisibility = (event) => {
        event.stopPropagation();
        event.preventDefault();
        setVisibile(!optionsVisible);
    }

    const toggleHalfHours = () => {
        setHalfHours(!halfHours);
    };

    const toggleCheckbox = (index) =>{
        setChecked(checked.map((val, i) => {
            return i === index ? !val : val; 
        }));
    }

    const generateLink = (event) => {
        event.stopPropagation();
        event.preventDefault();

        setLink('loading'); // hide the old link
        
        // prepare data from state
        var data = {
            meeting_len: meetingLen,
            buffer: buffer,
            workday_start: workdayStart,
            workday_end: workdayEnd,
            days_out: daysOut,
            weeks_out: weeksOut,
            weekdays: [],
            half_hours: halfHours
        };
        for (var i = 0; i < weekdays.length; i++) {
            const realDay = (i + 6) % 7;
            if (checked[i]) {
                data.weekdays.push(realDay);
            }
        }

        fetchData('/generate_link', data, 'Fetch link error',
              (data) => {
                    setLink(window.location.origin + "/schedule/" + data);
                    props.addLink(data);
              });
    }

    const lenInfo = "How long should the meeting be?";
    const bufferInfo = "How long should there be between this meeting " +
                        "and other events (before and after)?";
    const startInfo = "What is the earliest time this meeting can start?";
    const endInfo = "What is the latest time this meeting can end?";
    const daysOutInfo = "How many days in advance minimum should this meeting " + 
                            "be scheduled?";
    const weeksOutInfo = "How many weeks in advance can " +
                        "this meeting be scheduled (from today, regardless of " +
                        "when scheduling starts)?";
    const halfHourInfo = "Allow available time slots to start every half hour " +
                        "(instead of only every hour)?"
    return (
        <Jumbotron className="link-generator">
            <LinkGenHeader weeksOut={weeksOut}
                            toggleVisibility={toggleVisibility}
                            visible={optionsVisible} />
            <Form method="post" action="/generate_link">
                {optionsVisible &&
                <>
                    <Row>
                        <Col>
                            <GeneralFormGroup controlId="meeting-len"
                                                label="Meeting length (in minutes)"
                                                type="number"
                                                value={meetingLen}
                                                onChange={(event) => {
                                                   setLen(event.target.value);
                                                }}
                                                info={lenInfo}
                                                min="0" />
                        </Col>
                        <Col>
                            <GeneralFormGroup controlId="buffer"
                                                label="Buffer time (in minutes)"
                                                type="number"
                                                onChange={(event) => {
                                                    setBuffer(event.target.value);
                                                }}
                                                value={buffer}
                                                info={bufferInfo}
                                                min="0" />
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <GeneralFormGroup controlId="workday-start"
                                                label="Workday start time"
                                                type="time"
                                                onChange={(event) => {
                                                    setWorkdayStart(event.target.value);
                                                }}
                                                info={startInfo}
                                                value={workdayStart} />
                        </Col>
                        <Col>
                            <GeneralFormGroup controlId="workday-end"
                                                label="Workday end time"
                                                type="time"
                                                onChange={(event) => {
                                                    setWorkdayEnd(event.target.value);
                                                }}
                                                info={endInfo}
                                                value={workdayEnd} />
                        </Col>
                    </Row>
                    <Row>
                        <DaySelector weekdays={weekdays}
                                        checked={checked}
                                        toggleCheckbox={toggleCheckbox} />
                    </Row>
                    <Row>
                        <Col>
                            <GeneralFormGroup id="days-out"
                                                label="Minimum days in advance"
                                                type="number"
                                                min="0"
                                                onChange={(event) => {
                                                   setDaysOut(event.target.value);
                                                }}
                                                info={daysOutInfo}
                                                value={daysOut} />
                        </Col>
                        <Col>
                            <GeneralFormGroup id="weeks-out"
                                label="Up to this many weeks in advance"
                                                type="number"
                                                onChange={(event) => {
                                                    setWeeksOut(event.target.value);
                                                }}
                                                info={weeksOutInfo}
                                                min="1"
                                                value={weeksOut} />
                        </Col>
                    </Row>
                    <Row>
                        <Checked label="Schedule at half hours?"
                                 id="halfHours"
                                 info={halfHourInfo}
                                 checked={halfHours}
                                 toggle={toggleHalfHours} />
                    </Row>
                </>
                }
                <Row>
                    <Button variant="primary"
                            type="submit" 
                            onClick={generateLink}
                            className="centered">
                        Generate link!
                    </Button>
                </Row>
                <LinkDisplay link={link} />
            </Form>
        </Jumbotron>
        
    );
}

export default LinkGenerator;
