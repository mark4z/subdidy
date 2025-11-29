import json
import os
import urllib.request
from datetime import datetime, timezone, timedelta

def process():
    # 直接请求接口
    url = "https://qinqing.hangzhou.gov.cn/qqent/330109_078/api/admin/summation"
    print(f"Fetching data from {url}...")
    
    try:
        # 设置 User-Agent 避免被拦截 (虽然这个接口似乎不需要，但好习惯)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                print(f"Error: HTTP {response.status}")
                return
            data_bytes = response.read()
            current_data = json.loads(data_bytes.decode('utf-8'))
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # 保存最新的原始数据快照
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(current_data, f, ensure_ascii=False, indent=2)

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
