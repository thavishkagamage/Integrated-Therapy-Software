import React, { useRef, useState, useEffect } from "react";
import "./Chatbot.css"
import axios from "axios";

const Chatbot = () => {
  const [userInput, setUserInput] = useState("");
  const [conversation, setConversation] = useState([]);
  const messagesEndRef = useRef(null);
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
          { text: response.data.message, sender: "AI" },
        ]);
      } catch (error) {
        console.error("Error sending message:", error);
      }
    }
  };
  const scrollToBottom = () => {
    if (messagesEndRef.current) {
        messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };
  useEffect(() => {
    scrollToBottom();
  }, [conversation]);
  return (
    <div class="chat-window">
      <h1>Chat with our AI Bot</h1>
      <div class="chat-messages">
        <span class="start-message"> This is the beginning of your CBT chat session </span>
        {conversation.map((message, index) => (
          <div key={index} className={`${message.sender}-message message`}>
            <p key={index} className={message.sender}>
              {message.text}
            </p>
          </div>
        ))}
        <span ref={messagesEndRef} />
      </div>
      <div class="input-container">
        <input
          type="text"
          placeholder="Type your message here..."
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};
export default Chatbot;
