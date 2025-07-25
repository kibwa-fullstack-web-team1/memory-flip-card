import React from 'react';
import './ResultPopup.css'; // Assuming you'll have a CSS file for ResultPopup

function ResultPopup({ show, turns, elapsedTime, onPlayAgain }) {
  if (!show) return null;

  return (
    <div className="result-popup-overlay">
      <div className="result-popup-content">
        <h2>게임 종료!</h2>
        <p>총 턴 수: {turns}</p>
        <p>경과 시간: {elapsedTime}초</p>
        <button onClick={onPlayAgain}>다시 플레이</button>
      </div>
    </div>
  );
}

export default ResultPopup;