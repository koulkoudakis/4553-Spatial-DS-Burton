myStorage = window.localStorage;

let map = L.map("map").setView([0, 0], 1);
L.tileLayer("https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_nolabels/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attribution/">CartoDB</a>',
    subdomains: "abcd",
    maxZoom: 19
}).addTo(map);

// Add Layer Group
let layers = L.layerGroup().addTo(map);



function chooseRandomTarget(data) {
    url = "http://127.0.0.1:8080/randomCountry/"
    apiCall(url, saveTargetLocation)
}

function saveTargetLocation(data) {
    console.log(data);
    localStorage.setItem('target', JSON.stringify(data));
    console.log(JSON.parse(localStorage.getItem('target')));
}

function appendTableRow(name, location, distance, bearing, cardinal, arrow) {

    var table = document.getElementById("history");

    table.style.visibility = "visible";

    // Create an empty <tr> element and add it to the 1st position of the table:
    var row = table.insertRow();

    // Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
    var cell6 = row.insertCell(5);


    // Add some text to the new cells:
    cell1.innerHTML = name;
    cell2.innerHTML = location;
    cell3.innerHTML = distance;
    cell4.innerHTML = bearing;
    cell5.innerHTML = cardinal;
    cell6.innerHTML = arrow;

}

function getCardinal(degrees) {
    url = "http://127.0.0.1:8080/cardinal/" + String(degrees)
    apiCall(url, saveCardinal)
}

function saveCardinal(data) {
    console.log(data);
    localStorage.setItem('cardinal', JSON.stringify(data));
    console.log(JSON.parse(localStorage.getItem('cardinal')));
}

/**
 * populateDropDown: populates the dropdown list with countries
 * 
 * Params:
 *     data : array of countries
 */
function populateDropDown(data) {
    var select = document.getElementById("country");

    select.innerHTML = "";

    data.sort() // sort array of country names after request

    for (var i = 0; i < data.length; i++) {
        var opt = data[i];
        var el = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        select.appendChild(el);
    }
}

/**
 * getDropDownCountryName: returns the "selected" country name from the dropdown list
 * 
 * Params:
 *     None
 */
function getDropDownCountryName() {
    // get a reference to the dropdown element
    var e = document.getElementById("country");

    // pull the selected name from the list
    var name = e.options[e.selectedIndex].text;

    // return the name
    return name;
}

/**
 * updatePolygonCenter: Writes the center point passed in to a "hidden" element to be used 
 *      for the maps fly feature
 * 
 * Params:
 *     None
 */
function updatePolygonCenter(data) {
    console.log("updatePolygonCenter");
    console.log("DEBUG - DATA " + data);

    // add center point of polygon to local storage
    localStorage.setItem('polygonCenterPoint', data);

    let distance = localStorage.getItem('distance');
    console.log("distance: " + distance)

    // appendTableRow(localStorage.getItem('lastCountry'), localStorage.getItem('polygonCenterPoint'), distance)

    map.flyTo(L.latLng(data[1], data[0]), 5);
}

/**
 * updateLastCountryName: Print the last country selected on the web page at the proper element
 */
function updateLastCountryName(name) {
    console.log("updateLastCountryName");
    console.log(name);

    // save country name to local storage
    localStorage.setItem('lastCountry', name);
}


/**
 * showGeoJson: Show the geojson object we got from our Fast Api backend.
 */
function showGeoJson(data) {
    console.log("showGeoJson");

    result = {
        "type": "FeatureCollection",
        "features": [data['featureCollection']['features'][0]['feature']]
    }
    L.geoJSON(result).addTo(layers);

}

/**
 * apiCall: Calls the api we have been working on in order to "get" data and display it.
 * 
 * Params:
 *     string   url         : the route we want to call to get data
 *     function callback    : this is the function to run after we get the data
 */
function apiCall(url, callback) {
    fetch(url)
        .then(function (response) {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Something went wrong');
        })
        .then(function (data) {
            console.log(data);
            callback(data);
        }).catch((error) => {
            let message = "<h1>Error: Connecting to: " + url + "</h1>"
            message += "<h1>Is your API running?</h1>"
            document.getElementById("map").innerHTML = message;
            console.log(error)
        });
}

/**
 * apiGetCountryNames: Calls the api using the route to get all the country names.
 */
function apiGetCountryNames() {
    console.log("apiGetCountryNames");

    // url to get country names
    let url = "http://127.0.0.1:8080/country_names/";

    // call the api with the appropriate url and callback function to run on success
    apiCall(url, populateDropDown)
}

function storeDistanceBearing(data) {
    localStorage.setItem('distance', data['distance']);
    localStorage.setItem('bearing', data['bearing']);

    // Get cardinal direction
    cardinal = getCardinal(Math.round(data['bearing']))
    // json_cardinal = JSON.parse(cardinal)
    // console.log("DEBUG - cardinal" + cardinal)
    // console.log("DEBUG - cardinal" + cardinal)
    // console.log("DEBUG - cardinal" + localStorage.getItem('cardinal'))
    direction = JSON.parse(localStorage.getItem('cardinal'))

    appendTableRow(localStorage.getItem('lastCountry'), localStorage.getItem('polygonCenterPoint'), data['distance'], data['bearing'], direction['direction'], direction['img_tag'])

    // Handle game win
    if (data['distance'] == 0) { alert("WE HAVE A WINNAR - YOU WIN ONE(1) WORLD") }


}

/**
 * apiGetpolygonCenterPoint: Returns the "center point" of a given country. I'm using it so 
 *     I can pan and zoom to that location
 */
function apiGetpolygonCenterPoint(name) {
    console.log("apiGetpolygonCenter");

    console.log(name);
    // build the url to get the center of that country
    let url = "http://127.0.0.1:8080/countryCenter/" + name + "?raw=true";

    // call the api with the appropriate url and callback function to run on success
    apiCall(url, updatePolygonCenter)

    let target = localStorage.getItem('target')
    target = JSON.parse(target)


    let url2 = "http://127.0.0.1:8080/centroidRelations/?start=" + name + "&end=" + target['name'];

    console.log("DEBUG apiGetpolygonCenterPoint" + url2)

    // call the api with the appropriate url and callback function to run on success
    apiCall(url2, storeDistanceBearing)
}

/**
 * apiGetCountryPoly: Returns the "polygon" of the specified country (captured) from the
 *     dropdown list.
 */
function apiGetCountryPoly() {
    console.log("apiGetCountryPoly");

    let name = getDropDownCountryName();
    let url = "http://127.0.0.1:8080/country/" + name;

    // call api to get country shape and then send it to the showGeoJson function as a callback
    apiCall(url, showGeoJson);

    // now get the center point of the poly so we can pan and zoom
    apiGetpolygonCenterPoint(name);

    // save country name to local storage
    localStorage.setItem('lastCountry', name);

}

// add event listener to the submit button to call api and get a country polygon
document.getElementById("submit").addEventListener("click", apiGetCountryPoly);

// load drop down with existing country names
// erasing the old cars :) 
window.onload = function () {
    apiGetCountryNames();
    chooseRandomTarget();
};