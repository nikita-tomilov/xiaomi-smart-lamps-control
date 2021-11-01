var global_url = "";

function updateRGB(dev_id, jscolor_id) {
    const jscolor = document.getElementById(jscolor_id).value;
    // document.getElementById('rect').style.backgroundColor = '#' + jscolor;
    const rgbcolor = hexToRgb('#' + jscolor);
    httpGetAsync2(global_url + "colour/" + dev_id + "/" + rgbcolor.r + "/" + rgbcolor.g + "/" + String(parseInt(rgbcolor.b)));
}

function updateBrightness(dev_id, input_id) {
    const brightness = document.getElementById(input_id).value;
    httpGetAsync2(global_url + "brightness/" + dev_id + "/" + brightness);
}

function updateWB(dev_id, input_id) {
    const brightness = document.getElementById(input_id).value;
    httpGetAsync2(global_url + "wb/" + dev_id + "/" + brightness);
}

function switchState(dev_id, state) {
    httpGetAsync2(global_url + "switch/" + dev_id + "/" + state);
}

function switchFlow(dev_id, flow) {
    httpGetAsync2(global_url + "flow/" + dev_id + "/" + flow);
}

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function httpGetAsync2(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    console.log(theUrl);
    xmlHttp.open("GET", theUrl, true); // true for asynchronous
    xmlHttp.send(null);
}