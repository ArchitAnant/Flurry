import { create } from 'zustand';


const AZURE_KEY = process.env.REACT_APP_FLURRY_AZURE_KEY;

export const useTrendTopicViewModel = create((set) => ({
  trendTopic: '',
  updateTrendTopic: (newTopic) => set({ trendTopic: newTopic }),
}));

export const useTrendingValueList = create((set) => ({
  trendingList: null,
  updateTrendList: (newList) => set({ trendingList: newList }),
}));


export async function getTrendingList() {
  // https://flurryfunction.azurewebsites.net/api/trending?code=${AZURE_KEY}`
  try {
    const response = await fetch(`https://flurryfunction.azurewebsites.net/api/trending?code=${AZURE_KEY}`);
    const data = await response.json();
    console.log("Loaded trending data");
    const parsedList = data.reduce((acc, curr) => {
      const key = Object.keys(curr)[0];
      acc[key] = curr[key];
      return acc;
    }, {});
    useTrendingValueList.getState().updateTrendList(parsedList);
  } catch (err) {
    console.error("Failed to fetch trending data:", err);
  }
}

function isValidImageUrl(text) {
  return (text.startsWith('https://')||text.startsWith('http://')) && 
    (text.endsWith('.jpeg') || text.endsWith('.jpg') || text.endsWith('.png'));
}

export const fetchScriptData = async (trend) => {
  try {
    let response;
    if (isValidImageUrl(trend)) {
       console.log("Image URL detected");
      response = await fetch(`https://flurryfunction.azurewebsites.net/api/getimageresult?code=${AZURE_KEY}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: trend,
        }),
      });
    } else {
      console.log("Text Call detected");
      response = await fetch(`https://flurryfunction.azurewebsites.net/api/getscript?trend=${trend}&code=${AZURE_KEY}`, {
        method: "GET",
      });
    }


    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    console.log("Response for script data fetched successfully");

    // Flatten long_script if it's an array
    const longScriptText = Array.isArray(data.long_script)
      ? data.long_script.join(" ")
      : data.long_script;

    // Flatten short_script if it's an array
    const shortScriptText = Array.isArray(data.short_script)
      ? data.short_script.join(" ")
      : data.short_script;

    // Prepare response
    const to_resp = {
      long_script: longScriptText,
      short_script: shortScriptText,
      hook: data.hook_topics,
    };

    // If image analysis data exists
    if (data.famous_people) {
      to_resp.img_url = trend;
      console.log(data.famous_people)
      to_resp.famous_people = data.famous_people;
      to_resp.famous_places = data.famous_places;
      to_resp.text_in_image = data.text_in_image;
    }

    return to_resp;

    } catch (error) {
        console.error("Error fetching script data:", error);
        return null;
    }

};

export const checkAudioDownload = create((set) => ({
  isDownloadable: 0,
  downloadUrl: null,
  updateDownloadState: (newValue) => set({ isDownloadable: newValue }),
  updateDownloadUrl: (newUrl) => set({ downloadUrl: newUrl }),
}));


export const handleDownload = async (script, voiceCode) => {
  try {
    console.log(voiceCode)
    const response = await fetch(`https://flurryfunction.azurewebsites.net/api/getAudio?code=${AZURE_KEY}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        script: script,
        voice: voiceCode
      }),
    });

    if (!response.ok) {
      checkAudioDownload.getState().updateDownloadState(2);
      throw new Error('Failed to fetch audio file');
    } else {
      console.log("Audio file fetched successfully");
      checkAudioDownload.getState().updateDownloadState(1);

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      checkAudioDownload.getState().updateDownloadUrl(url);
      console.log("Audio file URL created successfully");
    }

  } catch (error) {
    console.error("Error downloading audio:", error);
    checkAudioDownload.getState().updateDownloadState(2);
  }
};


export const handleDownloadClick = () => {
  const { isDownloadable, downloadUrl } = checkAudioDownload.getState();
  if (isDownloadable === 1 && downloadUrl) {
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = 'audio.mp3'; // Specify the desired file name
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    checkAudioDownload.getState().updateDownloadState(0);
    checkAudioDownload.getState().updateDownloadUrl(null);
  }
  else if (isDownloadable === 2) {
    console.error("Audio file not available for download.");
  }
  else {
    console.error("Audio file not available for download.");
  }
}

