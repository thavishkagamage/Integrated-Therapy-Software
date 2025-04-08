import React, { useState, useEffect } from "react";
import axiosInstance from "../utils/axios"; // Ensure axios is properly set up
import { useNavigate } from 'react-router-dom';


const Goals = () => {
  const [goals, setGoals] = useState([]);
  const [goalInput, setGoalInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      navigate('/login'); // Redirect to login if no token found
    }
    fetchGoals();
  }, []);

  const getAuthHeaders = () => {
    const token = localStorage.getItem("accessToken");
    return token ? { Authorization: `Bearer ${token}` } : null;
  };

  const fetchGoals = async () => {
    setLoading(true);
    setError("");
    try {
      const headers = getAuthHeaders();
      if (!headers) throw new Error("No access token found.");

      const response = await axiosInstance.get("goals/", { headers });
      setGoals(response.data);
    } catch (err) {
      setError("Failed to fetch goals. Please try again.");
      console.error("Error fetching goals:", err);
    } finally {
      setLoading(false);
    }
  };

  const addGoal = async () => {
    if (!goalInput.trim()) return;

    if (goals.length >= 10) {
      setError("You can only have up to 10 goals.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const headers = getAuthHeaders();
      if (!headers) throw new Error("No access token found.");

      const response = await axiosInstance.post(
        "goals/",
        { name: goalInput },
        { headers }
      );

      setGoals([...goals, response.data]);
      setGoalInput("");
    } catch (err) {
      setError("Failed to add goal. Please try again.");
      console.error("Error adding goal:", err);
    } finally {
      setLoading(false);
    }
  };

  const deleteGoal = async (goalId) => {
    setLoading(true);
    setError("");
    try {
      const headers = getAuthHeaders();
      if (!headers) throw new Error("No access token found.");

      await axiosInstance.delete(`goals/${goalId}/`, { headers });
      setGoals(goals.filter((goal) => goal.id !== goalId));
    } catch (err) {
      setError("Failed to delete goal. Please try again.");
      console.error("Error deleting goal:", err);
    } finally {
      setLoading(false);
    }
  };

  // Your custom colors
  const customColors = {
    primaryBg: "#E0DDCF",
    secondaryBg: "#F1F0EA",
    accentColor: "#587B7F",
    highlightColor: "#729829",
    textLight: "#F1F0EA",
    textDark: "#587B7F",
  };

  return (
    <>
      <h1 className='mb-4 font-bold'>Goals</h1>
      <div
        className="max-w-3xl mx-auto p-6 rounded-lg shadow-lg"
        style={{ backgroundColor: customColors.accentColor }}
      >
        <h2
          className="text-2xl font-bold text-center"
          style={{
            fontFamily: "'Playfair Display', serif",
            color: customColors.textLight,
          }}
        >
          Your Goals
        </h2>
        {error && <p className="text-red-500 text-sm mb-3">{error}</p>}

        <div className="flex gap-2 mb-4">
          <input
            type="text"
            value={goalInput}
            onChange={(e) => setGoalInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') { addGoal() } } }
            placeholder="Enter a new goal..."
            className="flex-1 p-2 border rounded"
            style={{
              borderColor: customColors.accentColor,
              color: customColors.textDark,
            }}
          />
          <button
            onClick={addGoal}
            disabled={loading}
            className={`bg-[${customColors.highlightColor}] text-[${customColors.textLight}] px-4 py-2 rounded`}
          >
            {loading ? "Adding..." : "Add Goal"}
          </button>


        </div>

        {loading && <p className="text-gray-500">Loading goals...</p>}
        
        {goals.length === 0 ? (
          <p className='text-lg text-[--text-light] font-bold italic text-center'>You have no current goals.</p>
        ) : (
          <ul className="space-y-2">
            {goals.map((goal) => (
              <li
                key={goal.id}
                className="flex justify-between items-center p-3 border rounded-lg shadow-sm font-bold"
                style={{
                  backgroundColor: customColors.secondaryBg,
                  color: customColors.textDark,
                }}
              >
              <span>{goal.name}</span>
              <button
                onClick={() => deleteGoal(goal.id)}
                disabled={loading}
                className={`bg-[${customColors.primaryBg}] text-[${customColors.textDark}] hover:bg-[${customColors.primaryBg}] hover:text-red-500 px-4 py-2 rounded`}
              >
                Delete
              </button>

              </li>
            ))}
          </ul>
        )}
      </div>
    </>
  );
};

export default Goals;
