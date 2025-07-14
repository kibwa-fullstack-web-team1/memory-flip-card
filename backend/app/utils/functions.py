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