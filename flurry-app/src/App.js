import './App.css';
import HeroSection from './ui/hero/Hero';
import TrendingSection from "./ui/trending/Trending"
import ScriptSection from './ui/script/Scripts';

function App() {
  return (
    <div className="App bg-white flex flex-col min-h-screen ">
      <HeroSection />
      <TrendingSection />
      <ScriptSection />
      <Footer />
    </div>
  );
}

function Footer(){
  return(
      <footer
      className="w-full py-4 flex flex-row justify-end items-end mt-auto"
      >
        <div className='flex flex-col justify-start items-start ps-10 w-full '>
          <p className="text-[14px] text-darkGray">Flurry</p>
          <p className="text-[12px] text-lightGray">
            © {new Date().getFullYear()} Flurry. All rights reserved.
          </p>
        </div>
        <div className='flex flex-row items-end justify-end w-full pe-10'>
          <a
            href='https://github.com/ArchitAnant/Flurry'
            className="text-[12px] text-lightGray"
          >
            Disclaimer
          </a>
          <a
            href='https://github.com/ArchitAnant/Flurry'
            className="text-[12px] text-lightGray ps-10"
          >
            Github
          </a>
        </div>
      </footer>
  );
}

export default App;
