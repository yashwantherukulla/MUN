import React, { useState, useEffect } from 'react';
import { UserAuth } from '../app/context/AuthContext';
import { TypewriterEffectSmooth } from './ui/typewriter-effect';
import { useRouter } from 'next/navigation';
import axios from 'axios';

const Register = () => {
  const { user, googleSignIn, logOut } = UserAuth();
  const [loading, setLoading] = useState(true);
  const router = useRouter();
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
    if (user != null && user) {
      axios
        .post(
          'http://127.0.0.1:8001/email_sign_up',
          JSON.stringify({
            email: user.email,
          }),
          {
            headers: {
              'Content-Type': 'application/json',
            },
          }
        )
        .then((response) => {
          console.log(response);
        });
    }
  }, [user]);

  const words = [
    {
      text: 'Login Now',
      className: 'text-3xl',
    },
    {
      text: '& Register',
      className: 'text-3xl',
    },
    {
      text: 'to Join',
      className: 'text-3xl',
    },
    {
      text: 'SummitSync',
      className: 'text-blue-500 dark:text-blue-500 text-3xl',
    },
  ];

  return (
    <div className="flex items-center justify-center h-screen ">
      {loading ? null : !user ? (
        <div className="border border-blue-500 rounded-lg p-12 flex flex-col items-center justify-center w-[45rem]">
          <div className="w-98 ml-6 text-center text-white">
            <TypewriterEffectSmooth words={words} />
          </div>
          <button onClick={handleSignIn} className="p-2 cursor-pointer bg-blue-500 text-white rounded">
            Sign in with Google
          </button>
        </div>
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
