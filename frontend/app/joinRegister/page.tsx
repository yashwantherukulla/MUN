'use client';
import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import { UserAuth } from '../context/AuthContext';
import axios from 'axios';
import { useRouter } from 'next/navigation';

interface ResponseType {
  mun_list_reg: string[][];
}

interface ResponseType {
  mun_list_user: string[][];
}

const Pages = () => {
  const { user, googleSignIn, logOut } = UserAuth();
  const router = useRouter();
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

  const handleRegister = async (hostCode: string) => {
    axios
      .post(
        'http://127.0.0.1:8001/mun_reg',
        JSON.stringify({
          email: user.email,
          host_code: hostCode,
        }),
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      )
      .then((response) => {
        if (response.data.status === 'Success') {
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
        }
      });
  };

  const handleJoin = async (hostCode: string) => {
    router.push(`/room/${hostCode}`);
    localStorage.setItem('display_name', user.displayName);
  };

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
        <div className="flex flex-col justify-center items-center w-[50%] h-[84vh] m-2 border border-blue-500 rounded-[2rem] p-4 text-white">
          {response?.mun_list_reg.map((subArray, index) => (
            <div key={index} className="border border-white p-5 m-3 w-[75%] flex flex-row justify-between items-center">
              <p>{subArray[1]}</p>
              <button
                className="bg-blue-500 rounded-lg p-2"
                onClick={() => handleRegister(subArray[0])} // Pass the host code to the handler
              >
                Register Now
              </button>
            </div>
          ))}
        </div>
        <div className="flex flex-col justify-center items-center w-[50%] h-[84vh] m-2 border border-blue-500 rounded-[2rem] p-4 text-white">
          {response?.mun_list_user.map((subArray, index) => (
            <div key={index} className="border border-white p-5 m-3 w-[75%] flex flex-row justify-between items-center">
              <p>{subArray[1]}</p>
              <button
                className="bg-blue-500 rounded-lg p-2"
                onClick={() => handleJoin(subArray[0])} // Pass the host code to the handler
              >
                Join Now
              </button>
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default Pages;
