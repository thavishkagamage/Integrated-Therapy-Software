import React, { forwardRef, useEffect, useImperativeHandle } from 'react';
import axiosInstance from "../utils/axios";

const Agenda = forwardRef(({sessionNumber}, ref) => {
  
  useEffect(() => {

    const token = localStorage.getItem('accessToken');
    if (!token) {
      console.error("No access token found");
      return;
    }
    
    const fetchAgendaItems = async () => {
      // Testing getting agenda items
      const agendaItems = await axiosInstance.post(
        "get-agenda-items/",
        { 
          session_number: sessionNumber,
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      console.log(agendaItems.data.agenda)
    };

    fetchAgendaItems()
  }, []);

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
      Child component content.
    </div>
  );
});

// Using React.memo prevents re-render if props haven't changed.
export default React.memo(Agenda);
