import { useState, useContext, useEffect } from 'react';
import './App.css';
import DraftBoard from './components/DraftBoard';
import UserTeam from './components/UserTeam';
import PlayerBoard from './components/PlayerBoard';
import PreDraft from './components/PreDraft';
import WatingPage from './components/WaitingPage';
import { AuthProvider, AuthContext } from "./components/AuthContext";

function AppContent() {
  const [active, setActive] = useState('PlayerBoard');
  const [draftStarted, setDraftStarted] = useState(false);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    const checkDraftStatus = async () => {
      const res = await fetch("/getDraftStatus");
      const data = await res.json();
      if (data.status === "Running") {
          setDraftStarted(true);
      } else {
          setDraftStarted(false); // still 200, no red error in console
      }
    };

    const interval = setInterval(checkDraftStatus, 5000);
    checkDraftStatus(); // run once on mount

    return () => clearInterval(interval);
  }, []);

  // If not logged in → only show PreDraft
  if (!user) {
    return <PreDraft />;
  }

  // If logged in but draft hasn't started yet → Waiting Room
  if (!draftStarted) {
    return <WatingPage />;
  }

  // If logged in → show rest of app
  return (
    <>
      <div className="topBar">
        <button onClick={() => setActive('PlayerBoard')}>Draft</button>
        <button onClick={() => setActive('UserTeam')}>My Team</button>
        <button onClick={() => setActive('DraftBoard')}>Board</button>
      </div>
      {active === 'PlayerBoard' && <PlayerBoard />}
      {active === 'UserTeam' && <UserTeam />}
      {active === 'DraftBoard' && <DraftBoard />}
    </>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
