import React, { useRef, useState, useEffect } from "react";
import "./Chatbot.css";
import axiosInstance from "../utils/axios";
import { useLocation } from 'react-router-dom';

const Chatbot = () => {
  const [userInput, setUserInput] = useState("");
  const [conversation, setConversation] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [waitingForResponse, setWaitingForResponse] = useState(false);
  const [conversationFetched, setConversationFetched] = useState(false); // Track if conversation has been fetched
  const messagesEndRef = useRef(null);
  const hasMounted = useRef(false);
  const location = useLocation();

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const conversationIdFromUrl = queryParams.get('conversationId');
    if (conversationIdFromUrl) {
      setConversationId(conversationIdFromUrl);  // Set the conversationId if passed in URL
    }
  }, [location]);

  useEffect(() => {
    const createOrFetchConversation = async () => {
      if (loading || conversationFetched) return;  // Prevent repeated fetching if conversation is already fetched

      setLoading(true);
      try {
        const token = localStorage.getItem('accessToken');
        const userId = parseInt(localStorage.getItem('userId'));

        if (!token) {
          console.error("No access token found");
          return;
        }
        const queryParams = new URLSearchParams(location.search);
        const conversationId = queryParams.get('conversationId');
        console.log("conversationId", conversationId);
        if (conversationId) {
          // If a conversationId exists, fetch the existing conversation
          const response = await axiosInstance.get(`conversations/${conversationId}/`, {
            headers: { Authorization: `Bearer ${token}` }
          });

          // Update conversation state with the fetched messages
          setConversation(response.data.messages.map(message => ({
            text: message.content,
            sender: message.sender
          })));
        } else {
          // If no conversationId, create a new conversation
          const existingConversationsResponse = await axiosInstance.get(
            "conversations/",
            { headers: { Authorization: `Bearer ${token}` } }
          );

          const userConversations = existingConversationsResponse.data.filter(
            (conv) => conv.user === userId && conv.title.startsWith("New Conversation")
          );

          let conversationTitle = "New Conversation";
          if (userConversations.length > 0) {
            const existingNumbers = userConversations
              .map(conv => {
                const match = conv.title.match(/^New Conversation (\d+)$/);
                return match ? parseInt(match[1], 10) : 0;
              })
              .sort((a, b) => a - b);
            const nextNumber = existingNumbers.length ? existingNumbers[existingNumbers.length - 1] + 1 : 1;
            conversationTitle = `New Conversation ${nextNumber}`;
          }

          // Create a new conversation if none exists
          const newConversationResponse = await axiosInstance.post(
            "conversations/",
            { title: conversationTitle, user: userId },
            { headers: { Authorization: `Bearer ${token}` } }
          );
          setConversationId(newConversationResponse.data.id);  // Set new conversationId
          setConversation([]); // Clear existing conversation if creating new
        }

        // Mark conversation as fetched to prevent further calls
        setConversationFetched(true);

      } catch (error) {
        console.error("Error creating or fetching conversation:", error.response ? error.response.data : error.message);
      } finally {
        setLoading(false);
      }
    };

    createOrFetchConversation();
  }, [conversationId, loading, conversationFetched]);

  const sendMessage = async () => {
    setWaitingForResponse(true);
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

        const conversationHistory = newConversation.map(message => `${message.sender}: ${message.text}`).join('\n');

        // Fetch the session number and agenda items from the conversation
        const conversationResponse = await axiosInstance.get(`conversations/${conversationId}/`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        const { session_number, agenda_items } = conversationResponse.data;

        const response = await axiosInstance.post(
          "chatbot/",
          { 
            message: conversationHistory,
            session_number: session_number,
            agenda_items: agenda_items
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setConversation([
          ...newConversation,
          { text: response.data.message, sender: "ai" },
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
      } finally {
        setWaitingForResponse(false);
      }
    }
  };

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    if (hasMounted.current) {
      scrollToBottom();
    } else {
      hasMounted.current = true;
    }
  }, [conversation]);

  return (
    <div className="chat-window">
      <h1>Chat with our AI Bot</h1>
      <div className="chat-messages">
        <span className="start-message"> This is the beginning of your CBT chat session </span>
        {conversation.map((message, index) => (
          <span key={index} className={`${message.sender}-message message`}>
            {message.text}
          </span>
        ))}
        <div ref={messagesEndRef} />
        {waitingForResponse && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
          </div>
        )}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button className="send-button" disabled={waitingForResponse} onClick={sendMessage}>
          {waitingForResponse ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
