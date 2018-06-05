declare var code_editor: any;
declare var input_editor: any;

// API Endpoint for running code.
const run_endpoint = "/api/run";

/**
 * Runs the code given by the 'osabie-code' and 'osabie-input' input elements. After the response
 * is retrieved, the reponse of running the code is outputted.
 */
function run_code() {

    // Encode the code and input parameters
    var code = encodeURIComponent(code_editor.getValue());
    var input = encodeURIComponent(input_editor.getValue());
    var params; 
    
    // Construct the parameter body from the given parameters.
    if (code.length > 0 && input.length > 0) {
        params = "?code=" + code + "&input=" + input;
    } else if (code.length > 0) {
        params = "?code=" + code;
    } else if (input.length > 0) {
        params = "?input=" + input;
    } else {
        params = "";
    }

    // Clear out the warning description and set the status to running.
    WarningDescription.clear();
    Status.running();

    // Retrieve the JSON response from running the code.
    fetch(run_endpoint + params, {
        method: "POST"
    }).then(
        response => response.json()
    ).then(function(data) {
        document.getElementById("output-display").innerText = data['result']
        Status.pausing();
        WarningDescription.show(data['status']['code'], data['status']['truncated']);
    });
}

// Constants for modifying the info/warning description.
const TIMEOUT_MESSAGE = "the program was <span class='info-underline' title='The program exceeded the maximum timeout of 5 seconds and was therefore terminated.'>terminated</span>" 
const TRUNCATED_MESSAGE = "the output was <span class='info-underline' title='The output produced by the program exceeded the maximum size of 65536 bytes and was therefore truncated.'>truncated</span>"

/**
 * Class that represents the 'warning-description' text. This class contains
 * two different 'static' functions that mimic the dynamic changing of the
 * text by using the status received from the response. When showing, this
 * class makes sure that the correct information is shown after the response.
 */
class WarningDescription {

    /**
     * Show the warning description on the HTML page.
     * @param timeout - A boolean indicating whether the current program was timed out.
     * @param truncated - A boolean that indicates if the program output was truncated.
     */
    static show(timeout: boolean, truncated: boolean) {
        if (timeout === true && truncated === true) {
            document.getElementById("warning-description").innerHTML = "INFO: " + TIMEOUT_MESSAGE + " and " + TRUNCATED_MESSAGE + ".";
        } else if (timeout === true && truncated === false) {
            document.getElementById("warning-description").innerHTML = "INFO: " + TIMEOUT_MESSAGE + ".";
        } else if (timeout === false && truncated === true) {
            document.getElementById("warning-description").innerHTML = "INFO: " + TRUNCATED_MESSAGE + ".";
        }
    }

    /**
     * Clears the information of the warning description element.
     */
    static clear() {
        document.getElementById("warning-description").innerHTML = "";
    }
}

/**
 * Status class that dynamically handles the elements that need to change
 * on whether the current code execution request is still pending.
 */
class Status {

    /**
     * Method that handles the document elements while there is 
     * a pending code execution request.
     */
    static running() {
        document.getElementById("run-button").innerHTML = "Pause";
        document.getElementById("output-overlay").style.visibility = "visible";
        document.getElementById("output-display").innerText = "";
    }

    /**
     * Method that handles the document elements when there is no 
     * pending code execution request.
     */
    static pausing() {
        document.getElementById("run-button").innerHTML = "Run";
        document.getElementById("output-overlay").style.visibility = "hidden";
    }
}

document.onkeydown = function(event) {
    if (event.ctrlKey === true && event.key == "Enter") {
        run_code();
    }
}