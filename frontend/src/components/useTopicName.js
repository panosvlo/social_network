import { useState, useEffect } from 'react';
import api from '../services/api';

const useTopicName = (topicId) => {
  const [topicName, setTopicName] = useState('');

  useEffect(() => {
    const fetchTopicName = async () => {
      try {
        const response = await api.get(`/topics/${topicId}/`);
        setTopicName(response.data.name);
      } catch (error) {
        console.error('Error fetching topic name:', error);
      }
    };

    fetchTopicName();
  }, [topicId]);

  return topicName;
};

export default useTopicName;
