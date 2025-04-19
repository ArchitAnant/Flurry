import React from 'react';
import gsap from 'gsap';
import { useRef } from "react";
import { useTrendTopicViewModel } from '../ViewModel';

function ScriptSection() {
    const {updateTrendTopic, trendTopic} = useTrendTopicViewModel();
    const buttonRef = useRef(null);
    const buttonTextRef = useRef(null);
      const handleClick = () => {
        console.log(trendTopic);
        // Animate the button (e.g. scale bump)
        gsap.fromTo(
          buttonRef.current,
          { scale: 1 },
          { scale: 0.9, duration: 0.15, yoyo: true, repeat: 1, ease: 'expo.inOut' }
        );
      };

    return (
        <div className='flex flex-col min-w-screen justify-center items-center'>
            <div className='flex flex-row  mt-10'>
            <h1 className='text-black font-medium text-4xl mt-8'>Get your</h1>
            <h1 className='text-black font-medium ms-2 text-4xl bg-no-repeat bg-[url(ui/script/svgs/script_arrow.svg)] bg-contain bg-bottom py-8 '>
                scripts
            </h1>
            <h1 className='text-black font-medium ms-2 text-4xl mt-8 '>done!</h1>
            </div>
            <div className='flex flex-row'>
            <OutlinedTextField
            value={trendTopic}
            onChange={(e) => updateTrendTopic(e.target.value)}
            />
            <button 
            ref={buttonRef}
              onClick={handleClick}
              className='w-[180px] h-[55px] px-4 rounded-full bg-accent '>
                <div ref={buttonTextRef} className='font-medium text-white flex flex-row justify-center items-center'>
                  <h1 >Generate</h1>
                  <span class="material-symbols-outlined">
                  <h1 className=' ps-1'>arrow_right_alt</h1>
                  </span>
                </div>
              </button>
            </div>

        </div>
    );
}

function OutlinedTextField({ value, onChange }) {
    return (
      <div className="flex w-full max-w-sm justify-center items-center">
        <input
          type="text"
          value={value}
          onChange={onChange}
          placeholder='Write the script on?'
          className="ps-5 w-[300px] h-[55px] border-2 border-gray-300 text-accent font-medium rounded-full px-3 py-3 text-base focus:outline-none focus:border-accent transition-colors"
        />
      </div>
    );
  }

export default ScriptSection;