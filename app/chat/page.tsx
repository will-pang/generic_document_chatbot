"use client";

import { useEffect, useState } from 'react';
import { Chatbot } from '@/components/ChatWindow';

export default function ChatPage() {
  const [text, setText] = useState('');

  useEffect(() => {
    const fetchText = async () => {
      try {
        const response = await fetch('http://localhost:8000/retrieve/');
        if (!response.ok) {
          throw new Error('Failed to fetch text');
        }
        const data = await response.json();
        setText(data.text);
      } catch (error) {
        console.error('Error fetching text:', error);
      }
    };

    fetchText();
  }, []);

  return (
    <div className="flex h-screen">
      <div className="w-1/2 pt-14 pr-10">
        <p className="text-left p-0 overflow-auto h-full">
          {text}
        </p>
      </div>
      <div className="w-1/2 pt-10">
        <Chatbot />
      </div>
    </div>
  );
}
