import { useState } from 'react';
import Login from './Login';
import Register from './Register';

export default function Auth({ onAuth }: { onAuth: (token: string) => void }) {
  const [showLogin, setShowLogin] = useState(true);

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <button onClick={() => setShowLogin(true)} disabled={showLogin}>Login</button>
        <button onClick={() => setShowLogin(false)} disabled={!showLogin}>Register</button>
      </div>
      {showLogin ? (
        <Login onLogin={onAuth} />
      ) : (
        <Register onRegister={onAuth} />
      )}
    </div>
  );
}
