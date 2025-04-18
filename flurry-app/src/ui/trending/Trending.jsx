import React from "react";
import { useState } from 'react';
import underline from './svgs/trending_underline.svg'
import trendsData from './trends.json';
import { motion, AnimatePresence } from "framer-motion";

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

function TrendBadge({trend,onButtonclick}){
    return(
        <button 
        onClick={()=>{onButtonclick();console.log(trend)}}
        className='px-7 py-4 rounded-full items-center text-accent bg-lightGray bg-opacity-20'>
            {trend}
        </button>
    )
}

function TrendingSection() {
  const categories = Object.keys(Object.assign({}, ...trendsData)); 

  const [selectedCategory, setSelectedCategory] = useState(categories[0]);
  const [trendTopic, setTrendTopic] = "";

  const getTrendsForCategory = (category) => {
    const trendObj = trendsData.find(obj => obj[category]);
    return trendObj ? trendObj[category] : [];
  };
  const trends = getTrendsForCategory(selectedCategory);

    return(
        <div className="flex flex-col justify-center items-center">
            <div className="flex flex-col justify-center items-center pb-5">
                <h1 className="font-black text-medium text-lg">Trending Topics</h1>
                <img src={underline} alt="Logo" className="w-[140px]" />
            </div>
            <div className="flex flex-wrap justify-center gap-2 pb-4">
        {categories.map((cat) => (
          <RadioButton
            key={cat}
            name={cat.charAt(0).toUpperCase() + cat.slice(1)}
            selected={selectedCategory === cat}
            onButtonclick={() => setSelectedCategory(cat)}
          />
        ))}
      </div>
      <div className="flex flex-wrap justify-center gap-2 px-4 pt-5">
        <TrendingIdeas trends={trends} onTrendClick={setTrendTopic}/>
      </div>
      </div>
    );
}

function TrendingIdeas({trends,onTrendClick}){
  return(
    <AnimatePresence mode="wait">
        {trends.length === 0 ? (
          <motion.p
            key="no-trends"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
            className="text-darkGray text-sm italic mt-4"
          >
            No trends available for this category.
          </motion.p>
        ) : (
          trends.map((trend, idx) => (
            <motion.div
              key={trend}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2, delay: idx * 0.05 }}
            >
              <TrendBadge
                trend={trend}
                onButtonclick={() => onTrendClick}
              />
            </motion.div>
          ))
        )}
      </AnimatePresence>
  );
}


export default TrendingSection;