import json
import os
from datetime import datetime, timezone, timedelta

def process():
    # 读取最新抓取的数据
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            current_data = json.load(f)
    except FileNotFoundError:
        print("data.json not found")
        return
    except json.JSONDecodeError:
        print("data.json is not valid json")
        return

    if current_data.get('code') != '0000':
        print("API returned error code")
        return

    data_payload = current_data.get('data', {})
    
    # 构造要保存的记录
    # 使用 UTC+8 时区
    tz = timezone(timedelta(hours=8))
    record = {
        'timestamp': datetime.now(tz).isoformat(),
        'balance': float(data_payload.get('balance', 0)),
        'used': float(data_payload.get('used', 0)),
        'total': float(data_payload.get('total', 0)),
        'sum': data_payload.get('sum', 0)
    }

    # 读取历史数据
    history = []
    if os.path.exists('history.json'):
        try:
            with open('history.json', 'r', encoding='utf-8') as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

    # 追加新记录
    history.append(record)

    # 保存回 history.json
    with open('history.json', 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    print(f"Added new record. Total records: {len(history)}")

if __name__ == "__main__":
    process()
