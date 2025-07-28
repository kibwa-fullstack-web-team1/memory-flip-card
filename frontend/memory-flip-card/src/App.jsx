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
  const [gameStarted, setGameStarted] = useState(false); // 게임 시작 여부
  const [difficulty, setDifficulty] = useState(null); // 난이도 상태 추가 
  const [imageWarning, setImageWarning] = useState(false); // 이미지 부족 팝업
  const timerRef = useRef(null);
  // const gameEnded = startTime && endTime;

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

  useEffect(() => {
    // difficulty가 null이 아니고, cardImages가 로드되었을 때만 실행
    if (difficulty && cardImages.length > 0 && !gameStarted) {
      shuffleCards(cardImages);
    }
  }, [difficulty, cardImages, gameStarted]); // cardImages도 의존성 배열에 추가

  // 카드 셔플 함수
  const shuffleCards = (images) => {
    const difficultyToCount = {
      easy: 8,
      medium: 12,
      hard: 16,
    };
  const count = difficultyToCount[difficulty];
  const requiredPhotos = count / 2;

  if (images.length < requiredPhotos) {
    setImageWarning(true);
    return;
  }

  const selectedImages = images.slice(0, requiredPhotos); // 절반만 뽑아 페어로
  const shuffled = [...selectedImages, ...selectedImages]
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
  setGameStarted(false); // 게임 아직 시작 안 함. 3초 타이머 후에 true로 바뀜

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

  // 모든 카드 맞춘 경우 게임 완료 처리
  useEffect(() => {
    if (cards.length > 0 && cards.every(card => card.matched)) {
      clearInterval(timerRef.current);
      setTimeout(() => setShowResultPopup(true), 500);
      setGameStarted(false);
      saveGameResult(); // 게임 결과를 서버로 전송
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

  // 게임 다시 시작 (같은 난이도)
  // difficulty 상태를 건드리지 않음
  const handlePlayAgain = () => {
    shuffleCards(cardImages);
  };

  // 게임 전체 초기화 (난이도 선택으로 돌아감)
  const resetGame = () => {
    setGameStarted(false);
    setDifficulty(null);
    setCards([]);
    setChoiceOne(null);
    setChoiceTwo(null);
    setTurns(0);
    setElapsedTime(0);
    setIsWrongMatch(false);
    setShowResultPopup(false);
    if (timerRef.current) clearInterval(timerRef.current);
  };

  // 게임 결과 저장 API 호출
  const saveGameResult = async () => {
    try {
      await fetch("http://13.251.163.144:8020/games/records", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userId,
          score: cards.length / 2,
          attempts: turns,
          matches: cards.length / 2,
          duration_seconds: elapsedTime,
          difficulty: difficulty,
        }),
      });
    } catch (err) {
      console.error("게임 결과 저장 실패:", err);
    }
  };

  // 난이도 버튼 클릭 핸들러
  const handleDifficultySelect = (level) => {
    setDifficulty(level);
  };

  return (
    <div className="App">
      <h1>추억 카드 짝 맞추기</h1>

      {!gameStarted && !difficulty && (
        <div className="difficulty-buttons">
          <p>난이도를 선택하세요:</p>
          <button onClick={() => handleDifficultySelect("easy")}>쉬움 (8장)</button>
          <button onClick={() => handleDifficultySelect("medium")}>보통 (12장)</button>
          <button onClick={() => handleDifficultySelect("hard")}>어려움 (16장)</button>
        </div>
      )}


    {imageWarning && (
      <div className="popup warning">
        <p>이미지 장수가 부족합니다. 사진을 더 업로드해주세요.</p>
        <button onClick={() => setImageWarning(false)}>확인</button>
      </div>
    )}

      {/* 게임 시작 버튼 (카드가 준비되었지만 아직 시작 안 함) */}
      {!gameStarted && difficulty && !showResultPopup && (
        <button className="start-button" onClick={() => shuffleCards(cardImages)}>
          새 게임 시작
        </button>
      )}

      {/* 게임 끝나고 리셋 (난이도 선택 화면으로 돌아가기) */}
      {showResultPopup && (
        <button className="start-button" onClick={resetGame}>
          다시 시작하기 (처음으로)
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
