# 05/05/2021, 20:39 - Balaji: Emo ra nenu Inka cheyaledu avi
# example message format (24-hour)
# 24/11/2025, 11:17 am - Nishit: message
# example message format (12-hour with AM/PM)

import re
import pandas as pd

def preprocess(data, pattern=None):
    """
    Preprocess WhatsApp chat export.
    Auto-detects 24-hour or 12-hour (AM/PM) format.
    
    Args:
        data: Raw chat export text
        pattern: Optional format hint (24 or 12). If None, auto-detects.
    """
    # Auto-detect format if not specified
    if pattern is None:
        # Check if AM/PM appears in the first few lines
        sample = data[:1000].lower()  # Check more lines for better detection
        if ' am ' in sample or ' pm ' in sample or ' am-' in sample or ' pm-' in sample:
            pattern = 12
        else:
            pattern = 24
    
    # Define regex patterns for both formats
    if pattern == 12:
        # 12-hour format: "24/11/2025, 11:17 am - " or "24/11/2025, 11:17 AM - "
        date_pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(am|pm|AM|PM)\s-\s"
        datetime_format = "%d/%m/%Y, %I:%M %p - "
    else:
        # 24-hour format: "05/05/2021, 20:39 - "
        date_pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
        datetime_format = "%d/%m/%Y, %H:%M - "
    
    # Extract dates - use finditer to get full matches
    date_matches = list(re.finditer(date_pattern, data))
    dates = [match.group(0) for match in date_matches]
    
    # Split messages using positions
    messages = []
    for i, match in enumerate(date_matches):
        if i == 0:
            # First message: from start to first date
            if match.start() > 0:
                messages.append(data[:match.start()])
        else:
            # Subsequent messages: from end of previous date to start of current date
            prev_end = date_matches[i-1].end()
            messages.append(data[prev_end:match.start()])
    
    # Add last message after final date
    if date_matches:
        last_end = date_matches[-1].end()
        if last_end < len(data):
            messages.append(data[last_end:])
    
    # Remove empty first message if it exists
    if messages and not messages[0].strip():
        messages = messages[1:]
    
    # Ensure we have matching counts
    min_len = min(len(dates), len(messages))
    dates = dates[:min_len]
    messages = messages[:min_len]
    
    df = pd.DataFrame({
        "user_message": messages,
        "message_date": dates,
    })
    
    # Parse datetime based on format
    try:
        df["date"] = pd.to_datetime(df["message_date"], format=datetime_format)
    except ValueError as e:
        # Fallback: try to parse with errors='coerce' and then infer
        df["date"] = pd.to_datetime(df["message_date"], format=datetime_format, errors='coerce')
        # If still fails, try inferring
        if df["date"].isna().any():
            df["date"] = pd.to_datetime(df["message_date"], infer_datetime_format=True, errors='coerce')
    users = []
    messages = []
    for message in df["user_message"]:
        # split by : and split to user , message
        entry = re.split(r"([\w\W]+?):\s", message)
        if entry[1:]: # if it is user message (uname : message)
            users.append(entry[1])
            messages.append(entry[2])
        else: # if it is notification chat without user name
            users.append("notification")
            messages.append(entry[0])
    df["user"] = users
    df["message"] = messages
    df.drop(columns=["user_message"] , inplace=True)

    df["only_date"] = df["date"].dt.date
    df["year"] = df['date'].dt.year
    df["month_num"] = df["date"].dt.month
    df["month"] =  df['date'].dt.month_name()
    df["day"]=  df['date'].dt.day
    df["day_name"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    
    return df