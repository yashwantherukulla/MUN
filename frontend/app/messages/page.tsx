import React from 'react';

const Messages = () => {
    return (
        <div className="flex flex-row w-full text-white">
            <div className="flex flex-col justify-center items-center w-3/4 m-5">
                <div className="flex flex-col w-full m-3 border-gray-500 border-2 rounded-xl">
                    <h1 className="text-4xl font-bold m-5">Sort By</h1>
                    <div className="p-10 flex flex-col w-full">
                        <label className="mb-3 text-xl">Select Country</label>
                        <select className="mb-3 max-w-full border rounded p-2 bg-black">
                            <option>India</option>
                            <option>Austria</option>
                        </select>
                        <label className="mb-3 text-xl">Select Query Type</label>
                        <select className="mb-3 max-w-full border rounded p-2 bg-black">
                            <option>India</option>
                            <option>India</option>
                        </select>
                        <div className="w-40 justify-center items-center">
                            <button className="border border-green-500 text-green-500 rounded px-4 py-2">Submit</button>
                        </div>
                    </div>
                </div>
                <div className="flex flex-col w-full m-3 border-gray-500 border-2 rounded-xl">
                    <h1 className="text-4xl font-bold m-5">Received Message</h1>
                    <div className="p-10 flex flex-col max-w-full">
                        <label className="mb-3 text-xl">To</label>
                        <input className="mb-3 max-w-full border rounded p-2 bg-black"/>
                        <label className="mb-3 text-xl">From</label>
                        <input className="mb-3 max-w-full border rounded p-2 bg-black" />
                        <div className="mb-3">
                            <input type="checkbox" id="viaEB" name="viaEB" value="Via EB" className='bg-black' />
                            <label htmlFor="viaEB"> Via EB</label>
                        </div>
                        <label htmlFor="query" className="mb-3 text-xl">Chit Message:</label>
                        <textarea className="mb-3 border-gray-500 border-2 rounded-xl p-2 max-w-full bg-black"></textarea>
                        <div className="w-20 justify-center items-center">
                            <button className="border border-green-500 text-green-500 rounded px-4 py-2">Reply</button>
                        </div>
                    </div>
                </div>
            </div>
            <div className="flex flex-col justify-center items-center w-1/2 m-5 border-gray-500 border-2 rounded-xl">
                <div className="flex flex-row space-x-2 justify-between">
                    <button className="border border-red-500 text-red-500 rounded px-4 py-2">Upload Document</button>
                    <button className="border border-green-500 text-green-500 rounded px-4 py-2">Upload Image</button>
                </div>
            </div>
        </div>
    );
};

export default Messages;