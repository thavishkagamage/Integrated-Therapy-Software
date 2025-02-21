import React, { useRef, useState, useEffect } from "react";
import "./Chatbot.css";
import axiosInstance from "../utils/axios";
import { useLocation } from 'react-router-dom';

const Chatbot = () => {

  // These are variables we pass into the chatbot component (instead of using props)
  // 1. sessionId: the session number we will use to fetch the CBT instructions
  //    - when sessionId is 0 (default value) the user is in free chat
  // 2. convoId: the conversationId that identifies the conversation in the database
  //    - when convoId is null (default value) we create a new conversation 
  const location = useLocation();
  const { sessionId = 0, convoId = null} = location.state || {};

  const [userInput, setUserInput] = useState("");
  const [conversation, setConversation] = useState([]);
  const [conversationId, setConversationId] = useState(null); // may not need this since we use location.state
  const [loading, setLoading] = useState(false);
  const [waitingForResponse, setWaitingForResponse] = useState(false);
  const [conversationFetched, setConversationFetched] = useState(false); // Track if conversation has been fetched
  const messagesEndRef = useRef(null);
  const hasMounted = useRef(false);

  // useEffect(() => {
  //   const queryParams = new URLSearchParams(location.search);
  //   const conversationIdFromUrl = queryParams.get('conversationId');
  //   if (conversationIdFromUrl) {
  //     setConversationId(conversationIdFromUrl);  // Set the conversationId if passed in URL
  //   }

  //   setConversationId(convoId);  // Set the conversationId from location.state

  // }, [location]);

  useEffect(() => {
    const createOrFetchConversation = async () => {
      if (loading || conversationFetched) return;  // Prevent repeated fetching if conversation is already fetched

      console.log(`Chatbot Params: sessionId = ${sessionId} = convoId: ${convoId}`);

      setLoading(true);
      try {
        const token = localStorage.getItem('accessToken');
        const userId = parseInt(localStorage.getItem('userId'));

        if (!token) {
          console.error("No access token found");
          return;
        }
        // const queryParams = new URLSearchParams(location.search);
        // const conversationId = queryParams.get('conversationId');
        const conversationId = convoId; // using location.state instead of queryParams
        if (conversationId) {
          // If a conversationId exists, fetch the existing conversation
          const response = await axiosInstance.get(`conversations/${conversationId}/`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          console.log(response.data);

          // Update conversation state with the fetched messages
          setConversation(response.data.messages.map(message => ({
            text: message.content,
            sender: message.sender
          })));
        } else {
          // If no conversationId, create a new conversation
          const existingConversationsResponse = await axiosInstance.get( // DO WE NEED THIS? since we changed title format
            "conversations/",
            { headers: { Authorization: `Bearer ${token}` } }
          );

          const dateTime = new Date().toLocaleString('en-US', {
            year: '2-digit',
            month: 'numeric',
            day: 'numeric',
            hour: 'numeric',
            minute: '2-digit',
            hour12: true,
          });

          const title = (sessionId === 0) ? "Free Chat" : `Session ${sessionId}`;
          const conversationTitle = `${title} - ${dateTime}`;

          // const userConversations = existingConversationsResponse.data.filter(
          //   (conv) => conv.user === userId && conv.title.startsWith("New Conversation")
          // );

          // let nextNumber = 1;
          // if (userConversations.length > 0) {
          //   const existingNumbers = userConversations
          //     .map(conv => {
          //       const match = conv.title.match(/^New Conversation (\d+)$/);
          //       return match ? parseInt(match[1], 10) : 0;
          //     })
          //     .sort((a, b) => a - b);
          //   nextNumber = existingNumbers.length ? existingNumbers[existingNumbers.length - 1] + 1 : 1;
          // }
          // const conversationTitle = `New Conversation ${nextNumber} - ${dateTime}`;

          // Create a new conversation if none exists
          const newConversationResponse = await axiosInstance.post(
            "conversations/",
            { title: conversationTitle, user: userId, session_number: sessionId },
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
    // Set the waiting state to true before processing the message
    setWaitingForResponse(true);

    // Check if user input is not empty (after trimming) and a conversationId exists
    if (userInput.trim() && conversationId) {
      // Create a new conversation array including the user's message
      const newConversation = [
        ...conversation,
        { text: userInput, sender: "user" },
      ];
      // Update the conversation state with the new message
      setConversation(newConversation);
      // Clear the user input field
      setUserInput("");
      
      try {
        // Retrieve the access token from local storage
        const token = localStorage.getItem('accessToken');
        // If token is not found, log an error and exit the function
        if (!token) {
          console.error("No access token found");
          return;
        }

        // Create a conversation history string by joining each message with its sender
        const conversationHistory = newConversation
          .map(message => `${message.sender}: ${message.text}`)
          .join('\n');

        // Fetch the session number and agenda items for the conversation from the backend
        const conversationResponse = await axiosInstance.get(`conversations/${conversationId}/`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        // Destructure session_number and agenda_items from the response data
        const { session_number, agenda_items } = conversationResponse.data;

        // Send the conversation history to the chatbot endpoint along with session details
        const response = await axiosInstance.post(
          "chatbot/",
          { 
            message: conversationHistory,
            session_number: session_number,
            agenda_items: agenda_items
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        // Append the chatbot's response to the conversation state
        setConversation([
          ...newConversation,
          { text: response.data.message, sender: "ai" },
        ]);

        // Save the user's message to the database
        await axiosInstance.post(
          "messages/",
          { conversation: conversationId, sender: "user", content: userInput },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        // Save the AI's response to the database
        await axiosInstance.post(
          "messages/",
          { conversation: conversationId, sender: "ai", content: response.data.message },
          { headers: { Authorization: `Bearer ${token}` } }
        );
      } catch (error) {
        // Log any errors that occur during the process
        console.error("Error sending message:", error.response ? error.response.data : error.message);
      } finally {
        // Set waiting state to false once processing is complete, regardless of success or error
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
