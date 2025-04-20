import React, { useState,useRef,useEffect } from 'react';
import gsap from 'gsap';
import { useTrendTopicViewModel,fetchScriptData,checkAudioDownload,handleDownload,handleDownloadClick } from '../ViewModel';

function ScriptSection() {
  const { updateTrendTopic, trendTopic } = useTrendTopicViewModel();
  const [buttonText, setButtonText] = useState("Generate");
  const [showScripts, setShowScripts] = useState(false);
  const [loading, setLoading] = useState(false);

  const [hookWordList, setHookWordList] = useState([]);
  const [durationList, setDurationList] = useState([]);
  const [shortScript, setShortScript] = useState("");
  const [longScript, setLongScript] = useState("");

  const buttonRef = useRef(null);
  const hookWordsRef = useRef(null);
  const durationsRef = useRef(null);
  const searchSectionRef = useRef(null);
  const scriptSectionRef = useRef(null);

  
  const calculateDuration = (text) => {
    const wordsPerMinute = 130; // avg human speech
    const wordCount = text.split(" ").length;
    const minutes = wordCount / wordsPerMinute;
    return `${minutes.toFixed(1)} minutes`;
  };


      const handleClick = async () => {
        console.log(trendTopic);
        if(trendTopic === ""){
          alert("Please enter a topic");
          return;
        }
        setButtonText("Regenerate")
        setShowScripts(true)
        // Animate the button (e.g. scale bump)
        gsap.fromTo(
          buttonRef.current,
          { scale: 1 },
          { scale: 0.9, duration: 0.15, yoyo: true, repeat: 1, ease: 'expo.inOut' }
        );
        const result = await fetchScriptData(trendTopic);

        if (result) {
          setShortScript(result.short_script);
          setLongScript(result.long_script);
          setHookWordList(result.hook);
          console.log(shortScript)
          console.log(hookWordList)
          setDurationList([
            `${calculateDuration(result.short_script)}`,
            `${calculateDuration(result.long_script)}`
          ]);
          setLoading(false);
        }
          else {
            setHookWordList([]);
            setDurationList([]);
            setShortScript("Error fetching short script");
            setLongScript("Error fetching long script");
            setLoading(false);
          }

        gsap.to(searchSectionRef.current, {
          x: (-window.innerWidth/3)+50,
          duration: 2,
          yoyo: false,
          ease: "expo.inOut"
        });
        gsap.to(buttonRef.current, {
          x:(-window.innerWidth/4)+50,
          y: 70,
          duration: 2,
          yoyo: false,
          ease: "expo.inOut"
        });

          setTimeout(() => {
            gsap.fromTo(hookWordsRef.current, { opacity: 0 }, { opacity: 1, duration: 1.5, ease: "expo.in" });
            gsap.fromTo(durationsRef.current, { opacity: 0 }, { opacity: 1, duration: 1.5, ease: "expo.in" });
            gsap.fromTo(scriptSectionRef.current, { opacity: 0 }, { opacity: 1, duration: 1.5, ease: "expo.in" });
          }, 300);

        if (window.scrollY < 500) {
      setTimeout(() => {
        window.scrollTo({
          top: window.scrollY + 300,  
          behavior: "smooth",          
        });
      }, 500);  
    }
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
            <div ref={searchSectionRef} className='flex flex-row'>
            <OutlinedTextField
            value={trendTopic}
            onChange={(e) => updateTrendTopic(e.target.value)}
            />
            <button 
            ref={buttonRef}
              onClick={handleClick}
              className='w-[180px] h-[55px] px-4 rounded-full bg-accent '>
                <div className='font-medium text-white flex flex-row justify-center items-center'>
                  <h1 >{buttonText}</h1>
                  <span class="material-symbols-outlined">
                  <h1 className=' ps-1'>arrow_right_alt</h1>
                  </span>
                </div>
              </button>
            </div>
            {showScripts && (
        <div className='w-full flex flex-row'>
          {loading ? (
            <div className="flex justify-center items-center w-full h-[300px]">
              <h1 className="text-accent text-lg animate-pulse">Generating your script...</h1>
            </div>
          ) : (
            <>
              <div className='w-full flex flex-col'>
                <div ref={hookWordsRef} className='flex flex-col justify-start text-start mt-[120px] ms-10 ps-10'>
                  <h1 className='text-accent font-medium font-lg'>Hook Words</h1>
                  <div className="flex flex-wrap gap-2 mt-5 w-[300px]">
                    {hookWordList.length === 0 ? (
                      <p className="text-gray-500 text-sm italic">No hooks available.</p>
                    ) : (
                      hookWordList.map((word, idx) => (
                        <h1 key={idx} className='bg-accent bg-opacity-60 py-3 px-5 text-white rounded-full'>{word}</h1>
                      ))
                    )}
                  </div>
                </div>

                <div ref={durationsRef} className='flex flex-col justify-start text-start mt-[40px] ms-10 ps-10'>
                  <h1 className='text-accent font-medium font-lg'>Best Durations</h1>
                  <div className="flex flex-wrap gap-2 mt-5 w-[300px]">
                    {
                      durationList.length === 0 ? (
                        <p className="text-gray-500 text-sm italic">No durations available.</p>
                      ) : (
                        durationList.map((item, idx) => (
                      <h1 key={idx} className='bg-accent bg-opacity-60 py-3 px-5 text-white rounded-full'>{item}</h1>)
                      )
                    )}
                  </div>
                </div>
              </div>

              <div ref={scriptSectionRef} className='flex flex-col opacity-0 w-full pe-10 me-10'>
                <Script title={"Short Script"} script={shortScript} />
                <div className='h-10'></div>
                <Script title={"Long Script"} script={longScript} />
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

function OutlinedTextField({ value, onChange }) {
    return (
      <div className="flex w-full max-w-sm justify-center items-center ">
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

function SpeechRadioButton({name, onButtonclick,selected}){
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


function Script({ title, script }) {
  const { isDownloadable, downloadUrl, updateDownloadState, updateDownloadUrl } = checkAudioDownload();

  const [speechState, setSpeechState] = useState(0);
  const [voiceName, changeVoiceName] = useState("Quinn");

  const titleRef = useRef(null);
  const buttonTextRef = useRef(null);
  const contentRef = useRef(null);
  const audioRef = useRef(null);

  const voiceList = ["Quinn", "Nia", "Chip", "Arista", "Angelo"];

  const getTitleBar = (state) => {
    switch (state) {
      case 1: return "Choose a Voice:";
      case 2: return "Generating Audio";
      default: return title;
    }
  };

  const handlePlayAudio = (name) => {
    const lowerName = name.toLowerCase();

    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }

    const newAudio = new Audio(`/audio/${lowerName}-demo.wav`);
    audioRef.current = newAudio;
    newAudio.play().catch(err => {
      console.error("Error playing audio:", err);
    });
    newAudio.addEventListener('ended', () => {
      audioRef.current = null;
    });
  };

  const getButtonText = (state) => {
    switch (state) {
      case 1: return "Synthesize Audio";
      case 2:
        if (isDownloadable === 1) return "Download";
        if (isDownloadable === 2) return "Try Again";
        return "Generating...";
      default: return "Synthesize using AI";
    }
  };

  useEffect(() => {
    const animateElement = (ref, newText) => {
      if (ref.current) {
        gsap.to(ref.current, {
          opacity: 0,
          duration: 0.3,
          ease: "power1.out",
          onComplete: () => {
            ref.current.innerText = newText;
            gsap.set(ref.current, { visibility: "hidden" });
            setTimeout(() => {
              gsap.set(ref.current, { visibility: "visible" });
              gsap.fromTo(
                ref.current,
                { opacity: 0, y: 10 },
                { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }
              );
            }, 200);
          }
        });
      }
    };

    animateElement(titleRef, getTitleBar(speechState));
    animateElement(buttonTextRef, getButtonText(speechState));

    if (contentRef.current) {
      gsap.fromTo(
        contentRef.current,
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.6, delay: 0.2, ease: "power2.out" }
      );
    }
  }, [speechState, isDownloadable]);

  const voiceMap = {
    "Quinn": 0,
    "Nia": 1,
    "Chip": 2,
    "Arista": 3,
    "Angelo": 4
  };
  const handleBack = () => {
    setSpeechState((prev) => Math.max(prev - 1, 0));
  };
  const handleForward = () => {
    if (speechState === 1) {
      // onSynthesizeClick();
      if (isDownloadable === 0) {
        handleDownload(script, voiceMap[voiceName]);
      }
    } else if (speechState === 2) {
      if (isDownloadable === 1) {
        handleDownloadClick(downloadUrl);
        handleBack()
      } else if (isDownloadable === 2) {
        alert("Something went wrong while generating audio. Please try again.");
        handleBack()
      }
    }
    setSpeechState((prev) => Math.min(prev + 1, 2));
  };



  return (
    <div className='flex flex-col p-10 w-[800px] justify-center bg-lightGray bg-opacity-15 text-left translate-y-[-40px] rounded-2xl'>
      <div className='flex flex-row text-accent items-center'>
        {speechState !== 0 && (
          <span onClick={handleBack} className="material-symbols-outlined cursor-pointer">
            keyboard_backspace
          </span>
        )}
        <h1 ref={titleRef} className='text-accent font-medium text-base ps-2'>
          {getTitleBar(speechState)}
        </h1>
      </div>

      <div ref={contentRef} className="min-h-[150px] pt-4">
        {speechState === 0 && <h1>{script}</h1>}

        {speechState === 1 && (
          <>
            <h1 className='text-darkGray font-medium text-sm pb-8'>Tap on the name to hear them.</h1>
            <div className="flex flex-wrap max-w-[1000px] justify-center gap-2">
              {voiceList.map((voice) => (
                <SpeechRadioButton
                  key={voice}
                  name={voice}
                  selected={voiceName === voice}
                  onButtonclick={() => {
                    changeVoiceName(voice);
                    handlePlayAudio(voice);
                  }}
                />
              ))}
            </div>
          </>
        )}

        {speechState === 2 && (
          <div className='text-darkGray italic'>
            {isDownloadable === 0 && <p>Generating audio...</p>}
            {isDownloadable === 1 && <p>Audio is ready! Click Download.</p>}
            {isDownloadable === 2 && <p className="text-red-500">Error generating audio. Try again.</p>}
          </div>
        )}
      </div>

      <div className='flex flex-row w-full pt-10'>
        <div className='w-full'></div>
        <button
          onClick={handleForward}
          className='w-[300px] h-[55px] px-4 rounded-full bg-accent ml-auto disabled:opacity-50'
          disabled={speechState === 2 && isDownloadable === 0}
        >
          <div className='font-medium text-white flex flex-row justify-center items-center'>
            <h1 ref={buttonTextRef}>{getButtonText(speechState)}</h1>
            <span className="material-symbols-outlined ps-1">arrow_right_alt</span>
          </div>
        </button>
      </div>
    </div>
  );
}





export default ScriptSection;