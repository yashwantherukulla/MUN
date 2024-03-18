'use client';
import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import { UserAuth } from '../context/AuthContext';
import axios from 'axios';

interface ResponseType {
  mun_list_reg: string[][];
}

const Pages = () => {
  const { user, googleSignIn, logOut } = UserAuth();
  const [response, setResponse] = useState<ResponseType | null>(null);
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
    if (user) {
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
        })
        .catch((error) => {
          console.log(error);
        });
    }
    if (user) {
      axios
        .post(
          'http://127.0.0.1:8001/mun_page',
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
          setResponse(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }, [user]);

  return (
    <>
      <nav className="flex items-center justify-between bg-black p-6">
        <div className="flex items-center">
          <Image src="/logo.png" alt="Company Logo" width={30} height={30} className="mr-2" />
          <span className="text-white text-lg">SummitSync</span>
        </div>
        {!user ? (
          <button onClick={handleSignIn} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Sign In
          </button>
        ) : (
          <button onClick={handleSignOut} className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
            Sign Out
          </button>
        )}
      </nav>
      <div className="flex flex-row justify-center items-center h-max-screen">
        <div className="flex flex-col justify-center items-center w-[50%] m-2 border border-blue-500 rounded-[2rem] p-4">
          {response?.mun_list_reg.map((subArray, index) => (
            <p key={index}>{subArray[0]}</p>
          ))}
        </div>
        <div className="flex flex-col justify-center items-center w-[50%] m-2 border border-blue-500 rounded-[2rem] p-4"></div>
      </div>
    </>
  );
};

export default Pages;
