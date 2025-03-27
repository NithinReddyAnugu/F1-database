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

// Check if Firebase app is already initialized
let firebaseApp;
try {
  firebaseApp = firebase.app();
  console.log("Firebase app already initialized");
} catch (e) {
  // Initialize Firebase if not already initialized
  console.log("Initializing Firebase app");
  firebaseApp = firebase.initializeApp(firebaseConfig);
}

// Handle authentication state changes
firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    // User is signed in
    console.log("User is signed in:", user.email);
    
    // Get the token and verify with the backend
    user.getIdToken().then(function(token) {
      // Send token to backend for verification
      fetch('/token-verify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: token }),
      })
      .then(response => response.json())
      .then(data => {
        console.log('Token verification response:', data);
      })
      .catch(error => {
        console.error('Error verifying token:', error);
      });
    });
  } else {
    // User is signed out
    console.log("User is signed out");
  }
});

// Function to handle login with email/password
function loginWithEmail(email, password) {
  firebase.auth().signInWithEmailAndPassword(email, password)
    .then((userCredential) => {
      // Signed in 
      const user = userCredential.user;
      console.log("Logged in user:", user.email);
      window.location.href = '/';
    })
    .catch((error) => {
      console.error("Login error:", error.code, error.message);
      document.getElementById('login-error').textContent = error.message;
    });
}

// Function to handle logout
function logout() {
  firebase.auth().signOut()
    .then(() => {
      console.log("User signed out successfully");
      window.location.href = '/';
    })
    .catch((error) => {
      console.error("Logout error:", error);
    });
} 