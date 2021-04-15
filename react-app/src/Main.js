//----------------------------------------------------------------------------
// Main.js
// Author: Erin Vuong
// routing component, main pages
//----------------------------------------------------------------------------

import React from 'react';
import { Switch, Route } from 'react-router-dom';

// Import pages here
import Client from './Client';
import External from './External';

// use <Link to"##"><button></button></Link> from react-router-dom;

function Main()
{
    return (
        <Switch>
            <Route path="/schedule/:target" component={External} />
            <Route path="/">
                <Client />
            </Route>
        </Switch>
    );
}

export default Main;
