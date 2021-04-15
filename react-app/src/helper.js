//----------------------------------------------------------------------------
// helper.js
// Author: Erin Vuong
// JS helper methods
//----------------------------------------------------------------------------

function fetchData(url, body, errorStr, callback)
{
    const info = { method: 'POST' };
    if (body) {
        info.headers = { 'Content-Type': 'application/json' };
        info.body = JSON.stringify(body);
    }

    const retVal = fetch(url, info)
                    .then(response => response.json())
                    .then(data => callback(data))
                    .catch((error) => {
                        console.error(errorStr + ': ', error);
                    });
}

export { fetchData };