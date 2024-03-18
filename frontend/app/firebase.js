// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries
import { getAuth } from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDwG7rKumrQVbhqKPVBXVPkcHUdDe_0z_g",
  authDomain: "summit-sync-67953.firebaseapp.com",
  projectId: "summit-sync-67953",
  storageBucket: "summit-sync-67953.appspot.com",
  messagingSenderId: "17979615799",
  appId: "1:17979615799:web:14a0dc62ef8cf78a7eadb2",
  measurementId: "G-R1XYNP81E1"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
