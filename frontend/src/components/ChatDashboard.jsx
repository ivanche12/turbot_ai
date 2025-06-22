import React, { useEffect, useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Trash2 } from 'lucide-react';

const ChatDashboard = ({ onSelectSession }) => {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem("turbot_sessions")) || [];
    setSessions(saved);
  }, []);

  const createNewSession = () => {
    const newId = uuidv4();
    const updated = [newId, ...sessions];
    setSessions(updated);
    localStorage.setItem("turbot_sessions", JSON.stringify(updated));
    onSelectSession(newId);
  };

  const deleteSession = async (sessionId) => {
    const confirmDelete = window.confirm("Da li ste sigurni da želite da obrišete ovaj razgovor?");
    if (!confirmDelete) return;

    try {
      const response = await fetch(`http://localhost:8000/chat/history?session_id=${sessionId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        const updated = sessions.filter(id => id !== sessionId);
        setSessions(updated);
        localStorage.setItem("turbot_sessions", JSON.stringify(updated));
      } else {
        console.error('Greška pri brisanju sesije:', await response.text());
      }
    } catch (error) {
      console.error('Greška pri brisanju sesije:', error);
    }
  };

  return (
    <div className="p-4 space-y-6 overflow-y-auto h-full border-r border-gray-200 bg-white">
      <h1 className="text-xl font-bold text-gray-800">TurBot Razgovori</h1>

      <button
        onClick={createNewSession}
        className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        + Novi razgovor
      </button>

      <ul className="space-y-2">
        {sessions.map((id, i) => (
          <li key={id} className="relative">
            {/* Dugme za otvaranje razgovora */}
            <button
              onClick={() => onSelectSession(id)}
              className="w-full text-left px-4 py-2 pr-10 border rounded hover:bg-blue-50"
            >
              Razgovor #{sessions.length - i}
            </button>

            {/* Dugme za brisanje */}
            <button
              onClick={() => deleteSession(id)}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-gray-400 hover:text-red-600"
              title="Obriši razgovor"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ChatDashboard;