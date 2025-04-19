import React from "react";
import gsap from 'gsap';
import { useEffect, useRef, useState } from "react";
import underline from './svgs/trending_underline.svg'
import trendsData from './trends.json';
import { useTrendTopicViewModel } from '../ViewModel';



function RadioButton({name, onButtonclick,selected}){
    return(
        <button 
        onClick={() => {
          onButtonclick(name)
        }}
        className={`w-[150px] h-[50px] border rounded-full items-center ${selected ? 'bg-accent text-white' : 'bg-white text-accent border-accent'}`}>
            {name}
        </button>
    )

}


function TrendBadge({trend}){
  const {updateTrendTopic} = useTrendTopicViewModel();
  const buttonRef = useRef(null);
  const handleClick = () => {
    updateTrendTopic(trend);
  
    // Animate the button (e.g. scale bump)
    gsap.fromTo(
      buttonRef.current,
      { scale: 1 },
      { scale: 0.9, duration: 0.15, yoyo: true, repeat: 1, ease: 'expo.inOut' }
    );
  };
    return(
        <button 
        ref={buttonRef}
        onClick={handleClick}
        className='px-7 py-4 rounded-full items-center text-accent bg-lightGray bg-opacity-20'>
            {trend}
        </button>
    )
}

function TrendingSection() {
  const categories = Object.keys(Object.assign({}, ...trendsData)); 

  const [selectedCategory, setSelectedCategory] = useState(categories[0]);
  

  const getTrendsForCategory = (category) => {
    const trendObj = trendsData.find(obj => obj[category]);
    return trendObj ? trendObj[category] : [];

  };
  const trends = getTrendsForCategory(selectedCategory);

    return(
        <div className="flex flex-col justify-center items-center min-w-screen">
            <div className="flex flex-col justify-center items-center pb-5">
                <h1 className="font-medium text-lg">Trending Topics</h1>
                <img src={underline} alt="Logo" className="w-[140px]" />
            </div>
            <div className="flex flex-wrap max-w-[1000px] justify-center gap-2">
        {categories.map((cat) => (
          <RadioButton
            key={cat}
            name={cat.charAt(0).toUpperCase() + cat.slice(1)}
            selected={selectedCategory === cat}
            onButtonclick={() => setSelectedCategory(cat)}
          />
        ))}
      </div>
      <div className="w-full flex flex-wrap justify-center gap-2 px-4 mt-10">
        <TrendingIdeas trends={trends}/>
      </div>
      </div>
    );
}
function TrendingIdeas({ trends }) {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const el = containerRef.current;
    const children =el.children;
    

    // Animate the container's height to create a smooth transition
    gsap.fromTo(
      el,
      { height: el.offsetHeight/2 },
      {
        height: 'auto',
        duration: 1,
        ease: "power2.out",
      }
    );

    // Animate the individual trend items
    if (trends.length === 0) {
      gsap.fromTo(
        children[0],
        { opacity: 0, y: -10 },
        { opacity: 1, y: 0, duration: 0.3 }
      );
    } else {
      gsap.fromTo(
        children,
        { opacity: 0, scale: 0.9 },
        {
          opacity: 1,
          scale: 1,
          duration: 0.2,
          stagger: 0.05,
          ease: "power2.out"
        }
      );
    }
  }, [trends]);

  return (
    <div ref={containerRef} className="flex flex-wrap space-x-2 justify-center items-center overflow-hidden">
      {trends.length === 0 ? (
        <p className="text-darkGray text-sm italic mt-4">
          No trends available for this category.
        </p>
      ) : (
        trends.map((trend) => (
          <div key={trend} className="pt-4">
            <TrendBadge trend={trend} />
          </div>
        ))
      )}
    </div>
  );
}

export default TrendingSection;