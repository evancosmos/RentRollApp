import { initializeApp } from "https://www.gstatic.com/firebasejs/9.9.4/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.9.4/firebase-auth.js";

const firebaseConfig = {
    "apiKey": "AIzaSyC57KFHH7nQl_rAcfwmy7BGy8vdqFSmzLo",
    "authDomain": "rent-roll-webapp.firebaseapp.com",
    "databaseURL": "https://rent-roll-webapp-default-rtdb.firebaseio.com",
    "projectId": "rent-roll-webapp",
    "storageBucket": "rent-roll-webapp.appspot.com",
    "messagingSenderId": "510164293468",
    "appId": "1:510164293468:web:c3eb509a7894c96b0c9399",
    "measurementId": "G-VJQL7TQK4Q"
}

const app = initializeApp(firebaseConfig);

const auth = getAuth();

function createUser(){
    
    var email = document.getElementById("userEmail").value
    var password = document.getElementById("userPass").value
    createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
        // Signed in 
        const user = userCredential.user;
        // ...
    })
    .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        // ..
    });
}