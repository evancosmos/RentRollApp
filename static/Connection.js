//https://tms-dev-blog.com/python-backend-with-javascript-frontend-how-to/
//https://python.plainenglish.io/how-to-send-a-file-using-javascript-and-python-5038dc39707b
//https://medium.com/@nschairer/flask-api-authentication-with-firebase-9affc7b64715

var xhr = null;

function logInUser(form){
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = sendDataCallback;
    // asynchronous requests
    xhr.open("POST", "logIn", false);

    var userData = new FormData();
    userData.append("email", document.getElementById("userEmail").value);
    userData.append("password", document.getElementById("userPass").value);

    xhr.send(userData);

    dataDiv = document.getElementById('loggedInStatus');
    dataDiv.innerHTML = xhr.responseText;
}

function signUpUser(){
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = sendDataCallback;
    // asynchronous requests
    xhr.open("POST", "signUp", false);

    var userData = new FormData();
    userData.append("email", document.getElementById("userEmail").value);
    userData.append("password", document.getElementById("userPass").value);

    xhr.send(userData);

    dataDiv = document.getElementById('loggedInStatus');
    dataDiv.innerHTML = xhr.responseText;
}

function dataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("Listing data received!");
        dataDiv = document.getElementById('displayRoll');
        // Set current data text
        var obj = JSON.parse(xhr.response);
        dataDiv.innerHTML = JSON.stringify(obj, undefined, 2);
    }
    return;
}

function sendDataCallback() {
// Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 201) {
        console.log("Data creation response received!");
        dataDiv = document.getElementById('myfile');
        // Set current data text
        dataDiv.innerHTML = xhr.responseText;
    }
    return;
}

function retriveListings() {
    console.log("Get listings...");
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = dataCallback;
    // asynchronous requests
    xhr.open("GET", "retriveListings", true);
    // Send the request over the network
    xhr.send(null);
    return;
}

function giveError(e){
    dataDiv = document.getElementById('displayRoll');
    dataDiv.innerHTML = e;
}

function sendData(form) {
    let myPromise = new Promise(function(resolve, reject) {
        var formData = new FormData(form);

        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = sendDataCallback;
        // asynchronous requests
        xhr.open("POST", "fileSend", false);

        // Waiting text
        responseOut = document.getElementById('displayRoll');
        responseOut.innerHTML = "Reading the file...";
        
        xhr.send(formData);

        resolve(xhr.response);
    });

    myPromise.then(
        () => retriveListings()
    );

    return;
}