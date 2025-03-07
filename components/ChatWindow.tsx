"use client";

import { useState } from "react";

export function Chatbot() {
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>([]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { sender: "User", text: input }]);
      setInput("");
      // Simulate a bot response
      setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: "Bot", text: "This is a bot response." },
        ]);
      }, 1000);
    }
  };

  return (
    <div className="flex flex-col h-screen">
        <div className="flex mt-4">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-grow p-5 rounded-l-lg bg-gray-700"
          placeholder="Ask me about the medical document!"
        />
        <button
          onClick={handleSend}
          className="p-2 bg-gray-100 text-black rounded-r-lg"
        >
          Send
        </button>
      </div>
      <div className="flex-grow overflow-auto p-4 rounded-lg shadow-md">
        {messages.map((message, index) => (
          <div key={index} className={`mb-2 ${message.sender === "User" ? "text-right" : "text-left"}`}>
            <span className={`inline-block p-2 rounded-lg ${message.sender === "User" ? "bg-blue-500 text-white" : "bg-gray-300 text-black"}`}>
              {message.text}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}