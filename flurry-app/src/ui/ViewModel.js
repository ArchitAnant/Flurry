// src/viewmodels/useTrendTopicViewModel.js
import { create } from 'zustand';

export const useTrendTopicViewModel = create((set) => ({
  trendTopic: '',
  updateTrendTopic: (newTopic) => set({ trendTopic: newTopic }),
}));
