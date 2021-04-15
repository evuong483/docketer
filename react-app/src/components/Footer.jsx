//----------------------------------------------------------------------------
// Footer.jsx
// Author: Erin Vuong
// Footer component
//----------------------------------------------------------------------------

import React from 'react';

function Footer(props)
{
    return (
        <footer className="bg-light py-5">
            <div className="small text-center text-muted">
                {'Created for Junior IW (Spring 2021) by Erin Vuong. '}
                {'For help '}<a href={props.url} target="_blank">click here</a>.
            </div>
        </footer>
    );
}

export default Footer;
