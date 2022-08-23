//https://tms-dev-blog.com/python-backend-with-javascript-frontend-how-to/
//https://python.plainenglish.io/how-to-send-a-file-using-javascript-and-python-5038dc39707b

var xhr = null;

getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};

function dataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("User data received!");
        dataDiv = document.getElementById('displayRoll');
        // Set current data text
        dataDiv.innerHTML = xhr.responseText;
    }
}

function sendDataCallback() {
// Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 201) {
        console.log("Data creation response received!");
        dataDiv = document.getElementById('myfile');
        // Set current data text
        dataDiv.innerHTML = xhr.responseText;
    }
}

function getUsers() {
    console.log("Get users...");
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = dataCallback;
    // asynchronous requests
    xhr.open("GET", "http://localhost:5000/users", true);
    // Send the request over the network
    xhr.send(null);
}

function sendData(form) {
    var formData = new FormData(form);

    responseOut = document.getElementById('displayRoll');

    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = sendDataCallback;
    // asynchronous requests
    xhr.open("POST", "http://localhost:5000/fileSend", true); //http://localhost:5000/
    //xhr.setRequestHeader("Content-Type", "multipart/form-data");

    // Send the request over the network
    xhr.send(formData);
    getUsers();
}