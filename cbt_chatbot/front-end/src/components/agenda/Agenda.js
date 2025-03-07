import React, { forwardRef, useEffect, useImperativeHandle, useRef, useState } from 'react';
import axiosInstance from "../utils/axios";

const Agenda = forwardRef(({conversationId, sessionNumber}, ref) => {

  const agendaItems = useRef([])
  const [agendaItemsAndStatuses, setAgendaItemsAndStatuses] = useState(null);
  
  useEffect(() => {

    const token = localStorage.getItem('accessToken');
    if (!token) {
      console.error("No access token found");
      return;
    }

    const fetchSessionAgendaItems = async () => {
      try {
        // Get the sessions agenda items
        const agenda = await axiosInstance.post(
          "get-agenda-items/",
          { 
            session_number: sessionNumber,
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        // Create initial map of agenda items and statuses
        agendaItems.current = agenda.data.agenda;
        const agendaStatus = agendaItems.current.map((_, index) => (index === 0 ? 1 : 0));
        const itemsAndStatuses = new Map();

        agendaItems.current.forEach((item, index) => {
          itemsAndStatuses.set(item, agendaStatus[index]);
        });
        
        // Update state so the component re-renders
        setAgendaItemsAndStatuses(itemsAndStatuses);
        // console.log("AGENDA MAP:", itemsAndStatuses);
      } catch (error) {
        console.error("Error fetching agenda items:", error);
      }
    };

    fetchSessionAgendaItems()
  }, [sessionNumber]);

  // Define the function that you want to run
  const updateAgendaStatuses = (statuses) => {    
    // make new map with updated statuses
    const itemsAndStatuses = new Map();
    agendaItems.current.forEach((item, index) => {
      itemsAndStatuses.set(item, statuses[index]);
    });

    // Update state so the component re-renders
    setAgendaItemsAndStatuses(itemsAndStatuses);
    // console.log("UPDATED AGENDA MAP:", itemsAndStatuses);
  };

  // Expose the function via the ref
  useImperativeHandle(ref, () => ({
    update: updateAgendaStatuses
  }), []); // Empty dependency array means the handle doesn't change

  return (
    <div>
      {agendaItemsAndStatuses && [...agendaItemsAndStatuses].map(([key, value]) => {
        const textColor =
          value === 1 ? 'text-yellow-500' :
          value === 0 ? 'text-red-500' :
          value === 2 ? 'text-green-500' : '';
        return (
          <li key={key} className={'list-none'}>
            <span className={textColor}>{key}</span>
          </li>
        )
      })}
    </div>
  );
});

// Using React.memo prevents re-render if props haven't changed.
export default React.memo(Agenda);
