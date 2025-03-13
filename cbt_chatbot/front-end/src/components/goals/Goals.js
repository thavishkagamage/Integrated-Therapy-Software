import React, { useState, useEffect } from "react";
import axiosInstance from "../utils/axios"; // Ensure axios is properly set up

const Goals = () => {
  const [goals, setGoals] = useState([]);
  const [goalInput, setGoalInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
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

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold mb-4 text-center">Your Goals</h1>

      {error && <p className="text-red-500 text-sm mb-3">{error}</p>}

      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={goalInput}
          onChange={(e) => setGoalInput(e.target.value)}
          placeholder="Enter a new goal..."
          className="flex-1 p-2 border rounded"
        />
        <button
          onClick={addGoal}
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {loading ? "Adding..." : "Add Goal"}
        </button>
      </div>

      {loading && <p className="text-gray-500">Loading goals...</p>}

      <ul className="space-y-2">
        {goals.map((goal) => (
          <li
            key={goal.id}
            className="flex justify-between items-center p-3 border rounded-lg shadow-sm bg-gray-50"
          >
            <span>{goal.name}</span>
            <button
              onClick={() => deleteGoal(goal.id)}
              disabled={loading}
              className="text-red-500 hover:text-red-700"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Goals;
