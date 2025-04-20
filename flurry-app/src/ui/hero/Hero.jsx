import React from 'react';
import underline from './svgs/flurry-under.svg'
import graffiti from './svgs/hero-side.svg'
import shazam from './svgs/hero-shazam.svg'
import wordUnderline from './svgs/hero-word-under.svg'

function HeroSection() {
  return (
    <div className="relative w-screen overflow-hidden">
      <div className="absolute flex flex-col top-0 left-0 p-[35px]">
        <h1 className='text-base text-darkGray font-black'>FLURRY</h1>
        <img src={underline} alt="Logo" className="w-[73px]" />
      </div>
      <div className="absolute flex flex-col top-[-80px] right-[-170px]">
        <img src={graffiti} alt="Logo" className="w-[530px]" />
      </div>
      <div className='relative flex flex-row top-[-80px] left-[350px]'>
        <div className='absolute top-1/2 left-[-200px]  text-right'>
          <h1 className='text-darkGray text-4xl'>YOUR</h1>
          <h1 className='text-black font-black pt-2 text-5xl'>WORD</h1>
          <img src={wordUnderline} alt="Logo" className="w-[150px]" />
        </div>
        <img src={shazam} alt="Logo" className="w-[250px]" />
        <div className='absolute top-1/2 left-[250px] text-4xl text-left'>
          <h1 className='text-darkGray text-4xl'>OUR</h1>
          <h1 className='text-black font-black mt-2 pb-4 w-[140px]  text-5xl bg-no-repeat bg-[url(ui/hero/svgs/hero-idea-high.svg)] bg-contain'>IDEA.</h1>
        </div>
      </div>
    </div>
  );
}

export default HeroSection;
