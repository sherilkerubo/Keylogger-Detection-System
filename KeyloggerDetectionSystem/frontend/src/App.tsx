import React, { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { FaShieldAlt, FaKey, FaNetworkWired, FaBug } from 'react-icons/fa';
import './App.css'; // custom styles

interface LogResult {
  keystrokes: string[];
  processes: { pid: number; name: string }[];
  network: { src: string; dst: string; proto: number; sport: number; dport: number; layer: string }[];
  alerts: string[];
}

function App() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<LogResult | null>(null);
  const [history, setHistory] = useState<any[]>([]);

  const handleScan = async () => {
    setLoading(true);
    try {
      const response = await axios.get<LogResult>('http://127.0.0.1:5000/scan');
      setData(response.data);
      setHistory(prev => [{ timestamp: new Date().toLocaleString(), ...response.data }, ...prev]);
    } catch (error) {
      console.error('Scan failed', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <FaShieldAlt size={30} />
        <h1>Keylogger Detection Dashboard</h1>
        <button onClick={handleScan} className="scan-btn" disabled={loading}>
          {loading ? 'Scanning...' : '🔍 Start Scan'}
        </button>
      </header>

      {data && (
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid-container"
        >
          {/* Alerts */}
          <div className="card alert-card">
            <h3><FaBug /> Alerts</h3>
            {data.alerts.length > 0 ? (
              <ul>
                {data.alerts.map((alert, i) => (
                  <li key={i}>⚠️ {alert}</li>
                ))}
              </ul>
            ) : (
              <p className="success-text">✅ No threats found</p>
            )}
          </div>

          {/* Keystrokes */}
          <div className="card">
            <h3><FaKey /> Keystrokes</h3>
            <ul>
              {data.keystrokes.map((k, i) => <li key={i}>{k}</li>)}
            </ul>
          </div>

          {/* Network */}
          <div className="card">
            <h3><FaNetworkWired /> Network Traffic</h3>
            <ul>
              {data.network.map((n, i) => (
                <li key={i}>
                  [{n.layer}] {n.src}:{n.sport} ➝ {n.dst}:{n.dport} (proto {n.proto})
                </li>
              ))}
            </ul>
          </div>

          {/* Processes */}
          <div className="card">
            <h3>🧠 Processes</h3>
            <ul>
              {data.processes.map((p, i) => (
                <li key={i}>
                  <strong>{p.name || '[unknown]'}</strong> (PID: {p.pid})
                </li>
              ))}
            </ul>
          </div>
        </motion.div>
      )}

      {/* Sidebar for Scan History */}
      {history.length > 0 && (
        <div className="history-panel">
          <h4>🕒 Scan History</h4>
          <ul>
            {history.map((h, i) => (
              <li key={i}>
                <strong>{h.timestamp}</strong> – {h.alerts.length} alert(s)
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
