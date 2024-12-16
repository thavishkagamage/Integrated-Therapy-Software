import React, { useRef, useState, useEffect } from "react";
import "./Chatbot.css";
import axiosInstance from "../utils/axios";

const Chatbot = () => {
  const [userInput, setUserInput] = useState("");
  const [conversation, setConversation] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const createOrFetchConversation = async () => {
      try {
        const token = localStorage.getItem('accessToken');
        const userId = parseInt(localStorage.getItem('userId')); // Assuming you store the user ID in local storage
        if (!token) {
          console.error("No access token found");
          return;
        }

        // Fetch existing conversations
        const existingConversationsResponse = await axiosInstance.get(
          "conversations/",
          { headers: { Authorization: `Bearer ${token}` } }
        );

        const existingConversation = existingConversationsResponse.data.find(
          (conv) => conv.title === "New Conversation" && conv.user === userId
        );

        if (existingConversation) {
          setConversationId(existingConversation.id);
          // Load in conversation messages
          try {
            const response = await axiosInstance.get(`conversations/${existingConversation.id}/`, {
              headers: { Authorization: `Bearer ${token}` }
            });
            setConversation(response.data.messages.map(message => ({
              text: message.content,
              sender: message.sender
            })));
          } catch (error) {
            console.error('Error fetching messages:', error.response ? error.response.data : error.message);
          }
        } else {
          // Create a new conversation
          const response = await axiosInstance.post(
            "conversations/",
            { title: "New Conversation", user: userId },
            { headers: { Authorization: `Bearer ${token}` } }
          );
          setConversationId(response.data.id);
        }
      } catch (error) {
        console.error("Error creating or fetching conversation:", error.response ? error.response.data : error.message);
      }
    };

    createOrFetchConversation();
  }, []);

  const sendMessage = async () => {
    if (userInput.trim() && conversationId) {
      const newConversation = [
        ...conversation,
        { text: userInput, sender: "user" },
      ];
      setConversation(newConversation);
      setUserInput("");
      try {
        const token = localStorage.getItem('accessToken');
        if (!token) {
          console.error("No access token found");
          return;
        }
        const response = await axiosInstance.post(
          "chatbot/",
          { message: userInput },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setConversation([
          ...newConversation,
          { text: response.data.message, sender: "AI" },
        ]);

        // Save the message to the database
        await axiosInstance.post(
          "messages/",
          { conversation: conversationId, sender: "user", content: userInput },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        await axiosInstance.post(
          "messages/",
          { conversation: conversationId, sender: "ai", content: response.data.message },
          { headers: { Authorization: `Bearer ${token}` } }
        );
      } catch (error) {
        console.error("Error sending message:", error.response ? error.response.data : error.message);
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
    <div className="chat-window">
      <h1>Chat with our AI Bot</h1>
      <div className="chat-messages">
        <span className="start-message"> This is the beginning of your CBT chat session </span>
        {conversation.map((message, index) => (
          <div key={index} className={`${message.sender}-message message`}>
            {message.text}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="input-container">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;