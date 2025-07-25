import React, { useEffect, useState, useRef } from 'react';
import Card from './components/Card';
import ResultPopup from './components/ResultPopup';
import './App.css';

function App() {
  const [userId, setUserId] = useState("user2");
  const [cardImages, setCardImages] = useState([]);
  const [cards, setCards] = useState([]);
  const [turns, setTurns] = useState(0);
  const [choiceOne, setChoiceOne] = useState(null);
  const [choiceTwo, setChoiceTwo] = useState(null);
  const [disabled, setDisabled] = useState(false);
  const [showResultPopup, setShowResultPopup] = useState(false);
  const [isWrongMatch, setIsWrongMatch] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [gameStarted, setGameStarted] = useState(false); // 🟡 게임 시작 여부
  const timerRef = useRef(null);

  // 카드 이미지 API에서 불러오기
  useEffect(() => {
    const fetchCardImages = async () => {
      try {
        const response = await fetch(`http://13.251.163.144:8020/list/cards?user_id=${userId}`);
        if (!response.ok) throw new Error('카드 이미지 요청 실패');
        const imageUrls = await response.json();
        const formatted = imageUrls.map(url => ({ src: url, matched: false }));
        setCardImages(formatted);
      } catch (error) {
        console.error(error);
      }
    };

    fetchCardImages();
  }, [userId]);

  // 카드 이미지가 준비되었지만 자동 시작 제거
  // -> 새 게임 버튼으로 시작하게 하기 위해 자동 호출 제거

  // 카드 셔플 함수
  const shuffleCards = (images) => {
    const shuffled = [...images, ...images]
      .sort(() => Math.random() - 0.5)
      .map(card => ({ ...card, id: Math.random() }));

    setChoiceOne(null);
    setChoiceTwo(null);
    setCards(shuffled);
    setTurns(0);
    setElapsedTime(0);
    setIsWrongMatch(false);
    setShowResultPopup(false);
    setDisabled(true);
    setGameStarted(false); // 게임 아직 시작 안 함

    if (timerRef.current) clearInterval(timerRef.current);

    // 3초간 카드 보여주기
    setTimeout(() => {
      setDisabled(false);
      setGameStarted(true);
      timerRef.current = setInterval(() => {
        setElapsedTime(prev => prev + 1);
      }, 1000);
    }, 3000);
  };

  // 카드 클릭 처리
  const handleChoice = (card) => {
    if (!disabled && gameStarted) {
      if (card.id === choiceOne?.id) return; // 같은 카드 재클릭 방지
      choiceOne ? setChoiceTwo(card) : setChoiceOne(card);
    }
  };

  // 두 카드 비교
  useEffect(() => {
    if (choiceOne && choiceTwo) {
      setDisabled(true);
      if (choiceOne.src === choiceTwo.src) {
        setCards(prev =>
          prev.map(card =>
            card.src === choiceOne.src ? { ...card, matched: true } : card
          )
        );
        setIsWrongMatch(false);
        resetTurn();
      } else {
        setIsWrongMatch(true);
        setTimeout(() => {
          setIsWrongMatch(false);
          resetTurn();
        }, 1000);
      }
    }
  }, [choiceOne, choiceTwo]);

  // 모든 카드 맞춘 경우
  useEffect(() => {
    if (cards.length > 0 && cards.every(card => card.matched)) {
      clearInterval(timerRef.current);
      setTimeout(() => setShowResultPopup(true), 500);
      setGameStarted(false);
    }
  }, [cards]);

  // 턴 초기화
  const resetTurn = () => {
    setChoiceOne(null);
    setChoiceTwo(null);
    setTurns(prev => prev + 1);
    setDisabled(false);
    setIsWrongMatch(false);
  };

  const handlePlayAgain = () => {
    shuffleCards(cardImages);
  };

  return (
    <div className="App">
      <h1>추억 카드 짝 맞추기</h1>

      {/* 🟡 새 게임 시작 버튼 (게임 중이 아닐 때만) */}
      {!gameStarted && (
        <button className="start-button" onClick={() => shuffleCards(cardImages)}>
          새 게임 시작
        </button>
      )}

      <div className="card-grid">
        {cards.map(card => (
          <Card
            key={card.id}
            card={card}
            handleChoice={handleChoice}
            flipped={card === choiceOne || card === choiceTwo || card.matched || !gameStarted}
            disabled={disabled}
            isWrongMatch={isWrongMatch && (card === choiceOne || card === choiceTwo)}
          />
        ))}
      </div>

      <p>턴 수: {turns} | 경과 시간: {elapsedTime}초</p>

      <ResultPopup
        show={showResultPopup}
        turns={turns}
        elapsedTime={elapsedTime}
        onPlayAgain={handlePlayAgain}
      />
    </div>
  );
}

export default App;
