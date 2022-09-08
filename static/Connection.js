//https://tms-dev-blog.com/python-backend-with-javascript-frontend-how-to/
//https://python.plainenglish.io/how-to-send-a-file-using-javascript-and-python-5038dc39707b
//https://medium.com/@nschairer/flask-api-authentication-with-firebase-9affc7b64715
import { user } from "./Auth.js"

var xhr = null;

document.getElementById("upload-button").addEventListener('click', sendData);

function dataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("Listing data received!");
        var dataDiv = document.getElementById('displayRoll');
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
        var dataDiv = document.getElementById('myfile');
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
    if(user == null){
        xhr.setRequestHeader("UserSending", "notsignedin");
    }
    else{
        xhr.setRequestHeader("UserSending", user.uid);
    }
    // Send the request over the network
    xhr.send(null);
    return;
}

function giveError(e){
    dataDiv = document.getElementById('displayRoll');
    dataDiv.innerHTML = e;
}

function sendData() {
    let myPromise = new Promise(function(resolve, reject) {
        var form = document.getElementById("uploadForm");
        var formData = new FormData(form);

        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = sendDataCallback;
        // asynchronous requests
        xhr.open("POST", "fileSend", false);

        if(user == null){
            xhr.setRequestHeader("UserSending", "notsignedin");
        }
        else{
            xhr.setRequestHeader("UserSending", user.email);
        }
        

        // Waiting text
        var responseOut = document.getElementById('displayRoll');
        responseOut.innerHTML = "Reading the file...";
        
        xhr.send(formData);

        resolve(xhr.response);
    });

    myPromise.then(
        () => retriveListings()
    );

    return;
}