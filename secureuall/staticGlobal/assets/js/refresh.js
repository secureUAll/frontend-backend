/**
* This script allows to present user with feedback about how long the page was loaded
* To use, just insert element(s) with the class .refresh-counter. The text of those elements will be updated automatically.
* Example: <span class="refresh-counter"></span>
*
* The page will automatically reload every 5 minutes.
*/

// First threshold for 30 seconds, then every update every minute
const updateIntervals = {
    60: 30, // For first minute (60 seconds), update every 30 seconds
    300: 300, // For first 5 minutes, update every minute
    3600: 600, // For first hour, update every 10 minutes
    3700: 3600 // For the restant time, update every hour
}

// Current time
const rendered = Date.now();

function updateMessage(intervalId, intervalSpan) {
    // Compute time elapsed, in seconds
    const elapsedSecs = (Date.now()-rendered)/1000;
    // Compute message and update on view
    let elapsedText = "";
    if (elapsedSecs<60) {
        elapsedText = Math.round(elapsedSecs) + " seconds";
    } else if (elapsedSecs<3600) {
        elapsedText = Math.round(elapsedSecs/60) + " minutes";
    } else {
        elapsedText = Math.round(elapsedSecs/60/60) + " hours";
    }
    $(".refresh-counter").text("Updated " + elapsedText + " ago");
    // Update interval if threshold has been reached
    const intervalKey = Object.keys(updateIntervals).filter(x => x>elapsedSecs);
    if (intervalKey.length>0 && intervalSpan!=updateIntervals[intervalKey[0]]) {
        window.clearInterval(intervalId);
        const newIntervalId = setInterval(function(){
            updateMessage(newIntervalId, updateIntervals[intervalKey[0]]);
        }, updateIntervals[intervalKey[0]]*1000);
    }
}

$(document).ready(function () {
    // Default message
    $(".refresh-counter").text("Just updated");

    // Start counter for regular updates (every 30 seconds)
    const intervalId = setInterval(function(){
        updateMessage(intervalId, updateIntervals[Object.keys(updateIntervals)[0]]);
    }, updateIntervals[Object.keys(updateIntervals)[0]]*1000);

    // Start counter for page reload (5 minutes)
    setInterval(function(){
        window.location.reload();
    }, 1000*60*5);
});