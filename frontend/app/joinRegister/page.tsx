'use client';
import React from 'react';
import Image from 'next/image';

const pages = () => {
 
  return (
    <>
      <nav className="flex items-center justify-between bg-black p-6">
        <div className="flex items-center">
          <Image src="/logo.png" alt="Company Logo" width={30} height={30} />
          <span className="text-blue-500 font-bold text-xl ml-3">SummitSync</span>
        </div>
      </nav>
      <div className="flex flex-row justify-center items-center h-max-screen">
        <div className="flex flex-col justify-center items-center w-[50%] m-2 border border-blue-500 rounded-[2rem] p-4"></div>
        <div className="flex flex-col justify-center items-center w-[50%] m-2 border border-blue-500 rounded-[2rem] p-4"></div>
      </div>
    </>
  );
};

export default pages;
