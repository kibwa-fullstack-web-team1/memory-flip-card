import React from 'react';
import './Card.css';

function Card({ card, handleChoice, flipped, disabled, isWrongMatch }) {
  const handleClick = () => {
    if (!disabled) {
      handleChoice(card);
    }
  };

  // 조건에 따라 클래스 이름을 동적으로 결합
  const cardClasses = [
    'card',
    isWrongMatch ? 'wrong-match' : '',
    card.matched ? 'matched' : ''
  ].join(' ');

  return (
    <div className={cardClasses}>
      <div className={flipped ? 'flipped' : ''}>
        <img className="front" src={card.src} alt="card front" />
        <img
          className="back"
          src="/img/cover.png"
          onClick={handleClick}
          alt="card back"
        />
      </div>
    </div>
  );
}

export default Card;