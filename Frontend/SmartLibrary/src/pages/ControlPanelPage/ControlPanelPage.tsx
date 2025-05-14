import React from 'react';
import SideBar from '../../components/SideBar.js';
import ControlPanelCard from "@components/ControlPanelCard.js";



const ControlPanelPage = () => {
    return (
        <>
            <style>{`
        .layout {
          display: flex;
        }
        .main {
          flex-grow: 1;
          padding: 40px;
          background-color: #f4f6fa;
          min-height: 100vh;
        }
        .header {
          display: flex;
          align-items: center;
          gap: 10px;
          font-size: 24px;
          font-weight: bold;
          color: #1f3c88;
          margin-bottom: 30px;
          position:relative;
          left:290px;
        }
      `}</style>
            <div className="layout">
                <SideBar />
                <div className="main">
                    <ControlPanelCard />
                </div>
            </div>
        </>
    );
};
export default ControlPanelPage;