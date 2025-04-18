import React from 'react';
import { useState } from "react";

function ScriptSection() {
    const [trend, setTrend] = useState("");
    return (
        <div className='flex flex-col'>
            <div className='flex flex-row min-w-screen justify-center items-center mt-20'>
            <h1 className='text-black font-medium text-4xl pb-5'>Get your</h1>
            <h1 className='text-black font-medium ms-2 text-4xl bg-no-repeat bg-[url(ui/script/svgs/script_arrow.svg)] bg-contain bg-bottom py-8 pt-3'>
                scripts
            </h1>
            <h1 className='text-black font-medium ms-2 text-4xl pb-5'>done!</h1>
            </div>
            <OutlinedTextField
            label="Your Name"
            value={trend}
            onChange={(e) => setTrend(e.target.value)}
            />

        </div>
    );
}

function OutlinedTextField({ label, value, onChange, placeholder }) {
    return (
      <div className="relative w-full max-w-sm justify-center items-center">
        <input
          type="text"
          value={value}
          onChange={onChange}
          placeholder=" "
          className="peer w-full border-2 border-gray-300 text-darkGray rounded-full px-3 py-3 text-sm focus:outline-none focus:border-accent transition-colors"
        />
        <label
          className="absolute left-3 text-gray-500 text-xs  bg-white px-1"
        >
          {label}
        </label>
      </div>
    );
  }

export default ScriptSection;