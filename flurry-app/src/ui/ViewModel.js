// src/viewmodels/useTrendTopicViewModel.js
import { create } from 'zustand';

export const useTrendTopicViewModel = create((set) => ({
  trendTopic: '',
  updateTrendTopic: (newTopic) => set({ trendTopic: newTopic }),
}));

export const useTrendingValueList = create((set) => ({
  trendingList: null,
  updateTrendList: (newList) => set({ trendingList: newList }),
}));


export async function getTrendingList() {
  try {
    const response = await fetch('http://localhost:7071/api/trending');
    const data = await response.json();
    const parsedList = data.reduce((acc, curr) => {
      const key = Object.keys(curr)[0];
      acc[key] = curr[key];
      return acc;
    }, {});
    console.log("Parsed List", parsedList);
    useTrendingValueList.getState().updateTrendList(parsedList);
  } catch (err) {
    console.error("Failed to fetch trending data:", err);
  }
}

export const fetchScriptData = async (trend) => {
  try {
    // const response = await fetch(`http://localhost:7071/api/getScript`, {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json',
    //     'x-api-key': "apiKey" 
    //   },
    //   body: JSON.stringify({
    //     trend: trend
    //   })
    // });

    // if (!response.ok) {
    //   throw new Error(`API error: ${response.status}`);
    // }

    // const data = await response.json();

    // // Flatten long_script if it's an array
    // const longScriptText = Array.isArray(data.long_script)
    //   ? data.long_script.join(" ")
    //   : data.long_script;

    return {
      shortScript: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque neque ligula, molestie at elit id, accumsan efficitur felis. Cras vel nibh mi. Nam tincidunt eros nec justo pulvinar ultricies. Aliquam vitae tortor vitae sapien molestie facilisis vitae in augue. Integer ut mauris id elit tincidunt faucibus ut eu lorem. Proin volutpat odio eget metus luctus, efficitur gravida turpis fringilla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Quisque efficitur lacus mauris, sit amet vulputate felis rutrum non.",//data.short_script,
      longScript: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque neque ligula, molestie at elit id, accumsan efficitur felis. Cras vel nibh mi. Nam tincidunt eros nec justo pulvinar ultricies. Aliquam vitae tortor vitae sapien molestie facilisis vitae in augue. Integer ut mauris id elit tincidunt faucibus ut eu lorem. Proin volutpat odio eget metus luctus, efficitur gravida turpis fringilla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Quisque efficitur lacus mauris, sit amet vulputate felis rutrum non. Proin commodo vehicula mauris, eget rhoncus sapien. Vestibulum quis ante massa. Curabitur posuere in magna nec mollis. Donec. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque neque ligula, molestie at elit id, accumsan efficitur felis. Cras vel nibh mi. Nam tincidunt eros nec justo pulvinar ultricies. Aliquam vitae tortor vitae sapien molestie facilisis vitae in augue. Integer ut mauris id elit tincidunt faucibus ut eu lorem. Proin volutpat odio eget metus luctus, efficitur gravida turpis fringilla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Quisque efficitur lacus mauris, sit amet vulputate felis rutrum non. Proin commodo vehicula mauris, eget rhoncus sapien.",//data.longScriptText,
      hookTopics: ["Lorem ipsum","amet","dolor sit amet"]//data.hook_topics
    };

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


export const handleDownload = async (script,voiceCode) => {
  try {
    const response = await fetch(`http://localhost:7071/api/getAudio?script=${script}&voice=${voiceCode}&api_key=$`, {
      method: "GET",
    });

    if (!response.ok) {
      throw new Error('Failed to fetch audio file');
      checkAudioDownload.getState().updateDownloadState(2);
    }
    else{
      console.log("Audio file fetched successfully");
      checkAudioDownload.getState().updateDownloadState(1);
      
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      checkAudioDownload.getState().updateDownloadUrl(url);
      console.log("Audio file URL created successfully");
    }

  } catch (error) {
    console.error("Error downloading audio:", error);
  }
}

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

