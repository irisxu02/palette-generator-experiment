// onclick function for copying corresponding hex code for color boxes
function copyHex(code) {
    navigator.clipboard.writeText(code);
    alert("Copied " + code + " to clipboard!");
}