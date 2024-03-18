import React, { useState, useEffect } from 'react';
import { UserAuth } from '../app/context/AuthContext';

const Register = () => {
  const { user, googleSignIn, logOut } = UserAuth();
  const [loading, setLoading] = useState(true);

  const handleSignIn = async () => {
    try {
      await googleSignIn();
    } catch (error) {
      console.log(error);
    }
  };

  const handleSignOut = async () => {
    try {
      await logOut();
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    const checkAuthentication = async () => {
      await new Promise((resolve) => setTimeout(resolve, 50));
      setLoading(false);
    };
    checkAuthentication();
  }, [user]);

  useEffect(() => {
    if (user) {
      axios.post('127.0.0.1:8001/email_sign_up', {
        email: user.email
      })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
    }
  }, [user]);

  return (
    <div className="flex items-center justify-center h-screen">
      {loading ? null : !user ? (
        <button onClick={handleSignIn} className="p-2 cursor-pointer bg-blue-500 text-white rounded">
          Sign in with Google
        </button>
      ) : (
        <div>
          <p className="text-white">Welcome, {user.email}</p>
          <button onClick={handleSignOut} className="p-2 cursor-pointer bg-blue-500 text-white rounded">
           Sign Out
          </button>
        </div>
      )}
    </div>
  );
};

export default Register;
