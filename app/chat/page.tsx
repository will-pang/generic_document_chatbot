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
    <div>
      <h1>Chat Page</h1>
      <p>{text}</p>
    </div>
  );
}
