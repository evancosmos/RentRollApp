//For user authentication, NOT FOR DATABASE
import { initializeApp } from '../node_modules/firebase/app';
import * as fbAuth from '../firebasekeys.json';

const app = initializeApp(fbAuth);


//TODO: Fix the oath issue for imports

/* document.getElementById("signInBtn").addEventListener("click", signIn, false);

function signIn(){
    console.log("meep");

    var firebase = require('firebase');
    var firebaseui = require('firebaseui');

    var ui = new firebaseui.auth.AuthUI(firebase.auth());

    ui.start('#firebaseui-auth-container', {
        signInOptions: [
          firebase.auth.EmailAuthProvider.PROVIDER_ID
        ],
        // Other config options...
      });
} */
