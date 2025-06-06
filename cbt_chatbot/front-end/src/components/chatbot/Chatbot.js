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
  const [showSpinner, setShowSpinner] = useState(false);
  const [conversationFetched, setConversationFetched] = useState(false); // Track if conversation has been fetched
  const [showAgendaModal, setShowAgendaModal] = useState(false);
  
  // New ref for the chat container
  const chatContainerRef = useRef(null);
  const agendaRef = useRef(null);

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      navigate('/login'); // Redirect to login if no token found
    }

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

        // Check all conversations to see if the conversationId exists
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
            sender: message.sender,
            timestamp: message.created_at
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

        // update agenda component on page load/refresh as well
        if (agendaRef.current) {
          // Fetch the updated agenda items for the conversation from the backend
          const updatedConversation = await axiosInstance.get(`conversations/${conversationId}/`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          const updated_status = (updatedConversation.data.agenda_items);
          
          agendaRef.current.update(updated_status);
        }

      } catch (error) {
        console.error("Error creating or fetching conversation:", error.response ? error.response.data : error.message);
      } finally {
        setLoading(false);
      }
    };

    createOrFetchConversation();
  }, [conversationId, loading, conversationFetched, sessionId, convoId]);

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
    setShowSpinner(true);

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
            agenda_items: agenda_items,
            first_name: localStorage.getItem('first_name') || '',
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        // Create an array of paragraphs from the chatbot's response, slit on 2+ newlines
        const paragraphs = response.data.message.split(/\n\s*\n/).map(p => p.trim()).filter(Boolean);

        // Append the chatbot's response to the conversation state
        // setConversation([
        //   ...newConversation,
        //   { text: response.data.message, sender: "ai" },
        // ]);
        
        // Use a timeout to display each paragraph one by one
        const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
        const displayParagraphs = async () => {
          for (let i = 0; i < paragraphs.length; i++) {
            setConversation(prevConversation => [
              ...prevConversation,
              { text: paragraphs[i], sender: "ai" }
            ]);
            if (i === paragraphs.length - 1) {
              setShowSpinner(false);
            } else {
              await sleep(1000);
            }
          }
        };
        await displayParagraphs();

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
          
          agendaRef.current.update(updated_status);
        }
      } catch (error) {
        // Log any errors that occur during the process
        console.error("Error sending message:", error.response ? error.response.data : error.message);
        // add chat error message
        setConversation(prev => [
          ...prev,
          {
            text: "Something went wrong. Please try again.",
            sender: "ai"
          }
        ]);
      } finally {
        // Set waiting state to false once processing is complete, regardless of success or error
        setWaitingForResponse(false);
        setShowSpinner(false);
      }
    }
  };

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTo({
        top: chatContainerRef.current.scrollHeight,
        behavior: 'smooth'
      });
    }
  };
  

  useEffect(() => {
    scrollToBottom();
  }, [conversation]);

  return (
    <div className="chat-and-agenda-container">
      <div className="chat-window">
        <div className="chat-messages" ref={chatContainerRef}>
          <span className="start-message"> This is the beginning of your CBT chat session </span>
          {conversation
            .slice()
            .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
            .map((message, index) => (
              <span key={index} className={`${message.sender}-message message`}>
                <ReactMarkdown>{message.text}</ReactMarkdown>
              </span>
            ))}
          {showSpinner && (
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
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                // If we’re still waiting, do nothing
                if (waitingForResponse) {
                  e.preventDefault();
                } else {
                  // Otherwise, send the message
                  sendMessage();
                }
              }
            }}
          />
          <button className="send-button" disabled={waitingForResponse} onClick={sendMessage}>
            {waitingForResponse ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>

      <button 
        className="view-agenda-btn" 
        onClick={() => setShowAgendaModal(true)}>
        View Agenda
      </button>

      {sessionId !== 0 && (
        <div className="agenda-container">
          <Agenda ref={agendaRef} conversationId={convoId} sessionNumber={sessionId} />
        </div>
      )}

      {showAgendaModal && (
        <div className="agenda-modal">
          <button className="close-agenda-btn" onClick={() => setShowAgendaModal(false)}>
            Close Agenda
          </button>
          <Agenda ref={agendaRef} conversationId={convoId} sessionNumber={sessionId} />
        </div>
      )}
    </div>
  );
};

export default Chatbot;
