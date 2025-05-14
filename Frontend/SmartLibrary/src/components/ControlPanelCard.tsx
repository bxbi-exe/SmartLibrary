
import React from "react";
import { Link } from "react-router-dom";

const ControlPanelCard = () => {
    return (
        <div className="control-panel-container">
            <h1 className="welcome-title">Добредојде назад, професоре!</h1>
            <div className="card-grid">
                <Link to="/generated-tests" className="card card-purple">
                    <div className="card-icon">🧠</div>
                    <h2 className="card-title">Генерирани Тестови</h2>
                    <p className="card-desc">7 тестови подготвени за користење</p>
                </Link>
                <Link to="/dashboard" className="card card-blue">
                    <div className="card-icon">📄</div>
                    <h2 className="card-title">Вкупно Документи</h2>
                    <p className="card-desc">12 прикачени материјали</p>
                </Link>
            </div>

            <style>
                {`
          .control-panel-container {
            padding: 40px;
            background-color: #f5f6fa;
          }

          .welcome-title {
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 50px;
            text-align: center;
          
          }

          .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
          }

          .card {
            text-decoration: none;
            color: white;
            padding: 24px;
            border-radius: 20px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
          }

          .card:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.15);
          }

          .card-purple {
            background: linear-gradient(135deg, #8e44ad, #6c5ce7);
          }

          .card-blue {
            background: linear-gradient(135deg, #3498db, #00bcd4);
          }

          .card-icon {
            font-size: 36px;
            margin-bottom: 12px;
          }

          .card-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 8px;
          }

          .card-desc {
            font-size: 14px;
            line-height: 1.4;
          }
        `}
            </style>
        </div>
    );
};

export default ControlPanelCard;
