import React from 'react';
import {Link} from "react-router-dom";

const SideBar = () => {
    return (
        <>
            <style>{`
        .sidebar {
          width: 250px;
          background-color: #1f3c88;
          color: white;
          min-height: 100vh;
          padding: 20px;
          box-sizing: border-box;
        }
        .sidebar h1 {
          font-size: 20px;
          font-weight: bold;
          margin-bottom: 30px;
          display: flex;
          align-items: center;
          gap: 10px;
        }
        .menu-item {
          margin: 15px 0;
          display: flex;
          align-items: center;
          gap: 10px;
          cursor: pointer;
          transition: color 0.2s ease;
          color:white;
          text-decoration: none;
        }
        .menu-item:hover {
          color: #a3bffa;
        }
        .menu-item.logout {
          color: #f9c74f;
        }
      `}</style>
            <div className="sidebar">
                <h1>📚 Smart Library</h1>
                <Link to="/control-panel" className="menu-item">🏠 Контролна табла</Link>
                <Link to="/upload" className="menu-item">📤 Прикачи документ</Link>
                <Link to="/dashboard" className="menu-item">📁 Мои документи</Link>
                <Link to="/generated-tests" className="menu-item">🧠 Генерирани тестови</Link>
                <div className="menu-item logout">📕 Одјави се</div>
            </div>
        </>
    );
};

export default SideBar;
