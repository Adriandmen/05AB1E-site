class CookieHandler {

    /**
     * Gets the value of the cookie with the name given as a parameter.
     * @param name - The name of the cookie.
     */
    static getValueFromCookie(name: string): string {

        // Get the cookies of the current document.
        var parts = document.cookie.split("; " + name + "=");
        
        // If the cookie exists, return the value
        if (parts.length == 2) {
            return CookieHandler.parseCookie(parts.pop());
        }

        return undefined;
    }

    /**
     * Parse the value of the cookie such that it contains no escaped characters, etc.
     * @param cookieValue - The raw value of the cookie (possibly containing escaped characters and the like).
     */
    private static parseCookie(cookieValue: string): string {

        // The regex that matches \0\d{2}.
        var regex = /(\\0\d{2})/g;
        
        // While there is a match, replace the match in the cookie value
        // string with its actual character representation.
        var matches;
        do {

            // Check for the matches in the current cookie value.
            matches = regex.exec(cookieValue);
            if (matches === null) {
                break;
            }
            
            // Replace the octal representation with the actual ASCII character.
            var octalRepresentation = matches[1];
            var asciiChar = String.fromCharCode(parseInt(octalRepresentation.substr(1), 8)).trim();
            cookieValue = cookieValue.replace(octalRepresentation, asciiChar);
        } while (true);

        // Remove the surrounding quotes.
        return cookieValue.substr(1, cookieValue.length - 2);
    }
}