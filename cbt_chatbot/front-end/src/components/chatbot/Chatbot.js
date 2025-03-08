import React, { useRef, useState, useEffect } from "react";
import "./Chatbot.css";
import Agenda from "../agenda/Agenda"
import axiosInstance from "../utils/axios";
import { useLocation, useParams, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';

const Chatbot = () => {
  // Get parameters from URL instead of location.state
  const { sessionId: urlSessionId, conversationId: urlConversationId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  
  // Parse session and conversation IDs from URL or use from location.state as fallback
  const sessionId = urlSessionId ? parseInt(urlSessionId) : (location.state?.sessionId || 0);
  const convoId = urlConversationId ? urlConversationId : (location.state?.convoId || null);

  const [userInput, setUserInput] = useState("");
  const [conversation, setConversation] = useState([]);
  const [conversationId, setConversationId] = useState(convoId);
  const [loading, setLoading] = useState(false);
  const [waitingForResponse, setWaitingForResponse] = useState(false);
  const [conversationFetched, setConversationFetched] = useState(false); // Track if conversation has been fetched
  const messagesEndRef = useRef(null);
  const hasMounted = useRef(false);

  const agendaRef = useRef(null);

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

        // Check all cnversations to see if the conversationId exists
        const conversationId = convoId; // using location.state instead of queryParams
        const existingConversationsResponse = await axiosInstance.get(
          "conversations/",
          { headers: { Authorization: `Bearer ${token}` } }
        );
        const conversationExists = existingConversationsResponse.data.some(item => item.id == conversationId);
        
        if (conversationId && conversationExists){
          // If a conversationId and corresponding conversation exist, fetch the conversation
          const response = await axiosInstance.get(`conversations/${conversationId}/`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          console.log("RESPONSE:", response.data);

          // Update conversation state with the fetched messages
          setConversation(response.data.messages.map(message => ({
            text: message.content,
            sender: message.sender
          })));
        } else {
          // If no conversationId or conversation exist, create a new conversation
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

  // Update URL when conversation ID changes to make it bookmarkable/refreshable
  useEffect(() => {
    if (conversationId && !urlConversationId) {
      // Update URL without triggering a navigation
      navigate(`/sessions/chatbot/${sessionId}/${conversationId}`, { 
        replace: true,
        state: { sessionId, convoId: conversationId }
      });
    }
  }, [conversationId, navigate, sessionId, urlConversationId]);

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
            conversation_id: conversationId,
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

        // update agenda component
        if (agendaRef.current) {
          // Fetch the updated agenda items for the conversation from the backend
          const updatedConversation = await axiosInstance.get(`conversations/${conversationId}/`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          const updated_status = (updatedConversation.data.agenda_items);
          
          if (JSON.stringify(updated_status) !== JSON.stringify(agenda_items)) {
            agendaRef.current.update(updated_status);
          }
        }
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
    <>
      <div className="chat-window">
        <h1>Chat with our AI Bot</h1>
        <div className="chat-messages">
          <span className="start-message"> This is the beginning of your CBT chat session </span>
          {conversation.map((message, index) => (
            <span key={index} className={`${message.sender}-message message`}>
              <ReactMarkdown>{message.text}</ReactMarkdown>
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
      <Agenda ref={agendaRef} conversationId={convoId} sessionNumber={sessionId} />
    </>
  );
};

export default Chatbot;
