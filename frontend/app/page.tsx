"use client";
import React, {useState} from 'react'
import { motion } from 'framer-motion';
import { LampContainer } from '../components/ui/lamp';
import { AuthContextProvider } from '../app/context/AuthContext';
import Register from '@/components/Register';

const App = () => {
  const [showRegister, setShowRegister] = useState(false);

  const handleSignIn = () => {
    setShowRegister(true);
  };

  return (
    <AuthContextProvider>
      {showRegister ? (
        <Register /> // Render the Register component when showRegister is true
      ) : (
        <>
      <LampContainer className="flex items-center justify-center">
        <motion.h1
          initial={{ opacity: 0.5, y: 250 }}
          whileInView={{ opacity: 1, y: 130 }}
          transition={{
            delay: 0.3,
            duration: 0.8,
            ease: 'easeInOut',
          }}
          className="bg-gradient-to-br from-slate-300 to-slate-500 bg-clip-text text-center text-4xl font-medium tracking-tight text-transparent md:text-7xl pb-2 mt-10">
          SummitSync <br/> MUN&apos;s the Right Way
        </motion.h1>
      </LampContainer>
      <div className="space-x-8 flex flex-row justify-center items-center">
            <button onClick={handleSignIn} className="text-white border-2 rounded-lg border-blue-500 p-3 text-lg w-80">
              Get Started
            </button>
          </div>
          </>
      )}
    </AuthContextProvider>
  );
};

export default App;
