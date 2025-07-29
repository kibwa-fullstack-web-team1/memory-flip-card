import hashlib
from datetime import datetime

def format_timestamp(dt: datetime) -> str:
    """
    날짜/시간을 포맷팅합니다.
    
    Args:
        dt: 포맷팅할 datetime 객체
        
    Returns:
        str: 포맷팅된 날짜/시간 문자열
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def calculate_file_hash(file_contents: bytes) -> str:
    """
    파일 내용의 해시값을 계산합니다.
    
    Args:
        file_contents: 해시값을 계산할 파일 내용
        
    Returns:
        str: 파일의 해시값
    """
    return hashlib.sha256(file_contents).hexdigest()
