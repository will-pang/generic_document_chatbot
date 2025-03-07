"use client";

import { useEffect, useState } from 'react';

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
      <div className="w-1/2 p-4">
        <p className="text-3xl font-bold tracking-tight pb-4">📝 Document</p>
        <p className="text-left border border-white p-5 rounded-lg overflow-auto h-full">
          {text}
        </p>
      </div>
      <div className="w-1/2 p-4">
      <p className="text-3xl font-bold tracking-tight pb-4">💬 Chat</p>
        <p>This is the right half of the page.</p>
      </div>
    </div>
  );
}
