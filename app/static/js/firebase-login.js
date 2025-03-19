// Firebase configuration
// Replace with your own Firebase project configuration
const firebaseConfig = {
  apiKey: "AIzaSyBmpAX0rs_bwo7Zqe2vboSwEwbXX33mT3s",
  authDomain: "f1formula-f6f18.firebaseapp.com",
  projectId: "f1formula-f6f18",
  storageBucket: "f1formula-f6f18.firebasestorage.app",
  messagingSenderId: "458409824505",
  appId: "1:458409824505:web:a55a8a31b08adf0305d228",
  measurementId: "G-SZ1TPKM7Q2"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Handle authentication state changes
firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    // User is signed in
    console.log("User is signed in:", user.email);
  } else {
    // User is signed out
    console.log("User is signed out");
  }
}); 