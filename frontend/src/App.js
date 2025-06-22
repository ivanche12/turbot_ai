import React, { useState } from 'react';
import ChatDashboard from './components/ChatDashboard';
import TurBotChat from './components/TurBotChat';

function App() {
  const [currentSessionId, setCurrentSessionId] = useState(null);

  return (
    <div className="flex h-screen">
      {/* Leva strana – Sidebar */}
      <div className="w-80 border-r border-gray-200 bg-white">
        <ChatDashboard onSelectSession={(id) => setCurrentSessionId(id)} />
      </div>

      {/* Desna strana – Chat */}
      <div className="flex-1">
        {currentSessionId ? (
          <TurBotChat sessionId={currentSessionId} onBack={() => setCurrentSessionId(null)} />
        ) : (
          <div className="h-full flex items-center justify-center text-gray-500">
            Odaberite razgovor sa leve strane ili započnite novi.
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
