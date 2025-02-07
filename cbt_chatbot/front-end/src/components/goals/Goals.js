import React, { useState, useEffect } from "react";
import axiosInstance from "../utils/axios"; // Ensure this is configured to make API calls

const Goals = () => {
  const [goals, setGoals] = useState([]);
  const [goalInput, setGoalInput] = useState("");

  useEffect(() => {
    fetchGoals();
  }, []);

  const fetchGoals = async () => {
    try {
      const token = localStorage.getItem("accessToken");
      if (!token) {
        console.error("No access token found");
        return;
      }
      const response = await axiosInstance.get("goals/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setGoals(response.data);
    } catch (error) {
      console.error("Error fetching goals:", error);
    }
  };

  const addGoal = async () => {
    if (!goalInput.trim()) return;

    try {
      const token = localStorage.getItem("accessToken");
      if (!token) {
        console.error("No access token found");
        return;
      }
      const response = await axiosInstance.post(
        "goals/",
        { content: goalInput },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setGoals([...goals, response.data]);
      setGoalInput("");
    } catch (error) {
      console.error("Error adding goal:", error);
    }
  };

  const deleteGoal = async (goalId) => {
    try {
      const token = localStorage.getItem("accessToken");
      if (!token) {
        console.error("No access token found");
        return;
      }
      await axiosInstance.delete(`goals/${goalId}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setGoals(goals.filter((goal) => goal.id !== goalId));
    } catch (error) {
      console.error("Error deleting goal:", error);
    }
  };

  return (
    <div className="goals-container">
      <h1>Your Goals</h1>
      <div className="goal-input">
        <input
          type="text"
          value={goalInput}
          onChange={(e) => setGoalInput(e.target.value)}
          placeholder="Enter a new goal..."
        />
        <button onClick={addGoal}>Add Goal</button>
      </div>
      <ul className="goal-list">
        {goals.map((goal) => (
          <li key={goal.id}>
            {goal.content}
            <button onClick={() => deleteGoal(goal.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Goals;
