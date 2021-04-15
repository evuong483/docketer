//----------------------------------------------------------------------------
// Scheduler.jsx
// Author: Erin Vuong
// Coordinates scheduling components
//----------------------------------------------------------------------------
import React, { useState } from 'react';
import ConfirmMeeting from './ConfirmMeeting';
import Button from 'react-bootstrap/Button';
import AvailabilityCarousel from './AvailabilityCarousel';
import { fetchData } from '../helper';
import ScheduleSuccess from './ScheduleSuccess';
import { faPassport } from '@fortawesome/free-solid-svg-icons';

function Scheduler(props)
{
    const [modalVisible, setVisibility] = useState(false);
    const [confirmed, setConfirmed] = useState(false);
    const [showConfirmed, setShowConfirmed] = useState(false);
    const [guestName, updateName] = useState("");
    const [guestEmail, updateEmail] = useState("");
    const [guestNotes, updateNotes] = useState("");
    const [meetingStart, updateStart] = useState("");
    const [meetingEnd, updateEnd] = useState("");
    const [meetingBuffer, updateBuffer] = useState(0);
    const [meetingDate, updateDate] = useState("");
    const [prettyDate, updatePrettyDate] = useState("");

    const confirmMeeting = () => {
        const info = {
            start: meetingStart,
            end: meetingEnd,
            buffer: meetingBuffer,
            date: meetingDate,
            target: props.target,
            pretty_date: prettyDate,
            name: guestName,
            email: guestEmail,
            notes: guestNotes
        };

        fetchData('/schedule_meeting', info, 'Schedule meeting error',
            (data) => {
                if ('error' in data) {
                    props.setError(data.error);
            }
        });
        
        setVisibility(false);
        setConfirmed(true);
        setShowConfirmed(true);
    }

    // updates meeting info
    const updateMeetingInfo = (start, end, buffer, date, prettyDate) => {
        updateStart(start);
        updateEnd(end);
        updateBuffer(buffer);
        updateDate(date);
        updatePrettyDate(prettyDate);
    };

    return (
        <>
            { !confirmed ?
            <AvailabilityCarousel times={props.times}
                                  name={props.name}
                                  updateInfo={updateMeetingInfo}
                                  showConfirm={() => { 
                                      setVisibility(true)
                                  }} />
            : <p>Thank you for scheduling! You can close this page now.
                Check your email for meeting details.
                </p>
            }
            <ConfirmMeeting show={modalVisible}
                            hide={() => setVisibility(false)}
                            confirm={confirmMeeting}
                            changeName={updateName}
                            changeEmail={updateEmail}
                            changeNotes={updateNotes} />
            <ScheduleSuccess show={showConfirmed}
                             hide={() => setShowConfirmed(false)}
                             date={prettyDate}
                             start={meetingStart}
                             end={meetingEnd}
                             hostName={props.name}
                             email={guestEmail} />
        </>
    );
}

export default Scheduler;