import React, { forwardRef, useEffect, useImperativeHandle, useRef, useState } from 'react';
import axiosInstance from "../utils/axios";

const Agenda = forwardRef(({sessionNumber}, ref) => {

  // const agendaItems = useRef([])
  const [agendaItemsAndStatuses, setAgendaItemsAndStatuses] = useState(null);
  
  useEffect(() => {

    const token = localStorage.getItem('accessToken');
    if (!token) {
      console.error("No access token found");
      return;
    }

    const fetchSessionAgendaItems = async () => {
      try {
        // Testing getting agenda items
        const agenda = await axiosInstance.post(
          "get-agenda-items/",
          { 
            session_number: sessionNumber,
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        const agendaItems = agenda.data.agenda;
        const agendaStatus = agendaItems.map((_, index) => (index === 0 ? 1 : 0));
        const itemsAndStatuses = new Map();

        agendaItems.forEach((item, index) => {
          itemsAndStatuses.set(item, agendaStatus[index]);
        });
        
        // Update state so the component re-renders
        setAgendaItemsAndStatuses(itemsAndStatuses);
        console.log(agendaItemsAndStatuses);
      } catch (error) {
        console.error("Error fetching agenda items:", error);
      }
    };

    fetchSessionAgendaItems()
  }, [sessionNumber]);

  // Define the function that you want to run
  const runMyFunction = () => {
    console.log("Child function executed without re-rendering the component.");

    
    
  };

  // Expose the function via the ref
  useImperativeHandle(ref, () => ({
    runFunction: runMyFunction
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
