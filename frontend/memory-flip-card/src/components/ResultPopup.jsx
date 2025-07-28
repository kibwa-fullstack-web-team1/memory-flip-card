import React from 'react';
import './ResultPopup.css'; // Assuming you'll have a CSS file for ResultPopup

function ResultPopup({ show, turns, elapsedTime, onPlayAgain, onResetGame }) {
  if (!show) return null;

  return (
    <div className="result-popup-overlay">
      <div className="result-popup-content">
        <h3>축하합니다!</h3>     
        <h2>게임 완료!</h2>
        <p>총 턴 수: {turns}</p>
        <p>소요 시간: {elapsedTime}초</p>
        <button onClick={onPlayAgain}>게임 다시하기</button>
        <button onClick={onResetGame}>처음 화면으로</button>
      </div>
    </div>
  );
}

export default ResultPopup;