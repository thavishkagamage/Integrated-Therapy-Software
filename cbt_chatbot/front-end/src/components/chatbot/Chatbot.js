// src/Chatbot.js
import React, { useState } from "react";
import axios from "axios";
const Chatbot = () => {
  const [userInput, setUserInput] = useState("");
  const [conversation, setConversation] = useState([]);
  const sendMessage = async () => {
    if (userInput.trim()) {
      const newConversation = [
        ...conversation,
        { text: userInput, sender: "user" },
      ];
      setConversation(newConversation);
      setUserInput("");
      try {
        const response = await axios.post(
          "http://localhost:8000/api/chatbot/",
          { message: userInput }
        );
        setConversation([
          ...newConversation,
          { text: response.data.message, sender: "bot" },
        ]);
      } catch (error) {
        console.error("Error sending message:", error);
      }
    }
  };
  return (
    <div>
      <h1>Chat with our AI Bot</h1>
      <div>
        {conversation.map((message, index) => (
          <p key={index} className={message.sender}>
            {message.text}
          </p>
        ))}
      </div>
      <input
        type="text"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        onKeyPress={(e) => e.key === "Enter" && sendMessage()}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};
export default Chatbot;
