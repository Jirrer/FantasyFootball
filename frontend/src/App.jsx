import { useState, useContext } from 'react';
import './App.css';
import DraftBoard from './components/DraftBoard';
import UserTeam from './components/UserTeam';
import PlayerBoard from './components/PlayerBoard';
import PreDraft from './components/PreDraft';
import { AuthProvider, AuthContext } from "./components/AuthContext";

function AppContent() {
  const [active, setActive] = useState('PlayerBoard');
  const { user } = useContext(AuthContext);

  // If not logged in → only show PreDraft
  if (!user) {
    return <PreDraft />;
  }

  console.log(user)

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
