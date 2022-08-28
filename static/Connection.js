//https://tms-dev-blog.com/python-backend-with-javascript-frontend-how-to/
//https://python.plainenglish.io/how-to-send-a-file-using-javascript-and-python-5038dc39707b

var xhr = null;

function dataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("User data received!");
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

function getUsers() {
    console.log("Get users...");
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = dataCallback;
    // asynchronous requests
    xhr.open("GET", "users", true);
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
        xhr.open("POST", "fileSend", true);
        //xhr.setRequestHeader("Content-Type", "multipart/form-data");

        // Waiting text
        responseOut = document.getElementById('displayRoll');
        responseOut.innerHTML = "Reading the file...";
        
        xhr.send(formData);

        resolve(xhr.response);
    });

    myPromise.then(
        () => getUsers()
    );

    return;
}