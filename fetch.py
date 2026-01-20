import requests
import re
from bs4 import BeautifulSoup


TARGET_ROOM_KEYWORDS = [
    "庭園露天風呂付和室",
    "80"
]


def fetch_planlist_html(
    date="2026-02-25 00:00:00",
    nights=1
):
    """
    请求 /planlist/search，返回 planList HTML 字符串
    """
    url = "https://reserve.489ban.net/client/shikotsuko-daiichi/0/planlist/search"

    params = {
        "date": date,
        "numberOfNights": nights,
        "roomCount": 1,
        "guests[39602][adult]": 0,
        "guests[39603][adult]": 0,
        "meal_condition": 0,
        "searchTagMode": 0,
        "priceMin": 0,
        "priceMax": 99999999,
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept": "application/json",
        "Referer": "https://reserve.489ban.net/",
    }

    resp = requests.get(url, params=params, headers=headers, timeout=15, verify=False)
    resp.raise_for_status()

    data = resp.json()
    return data.get("planList", "")


def find_target_plan_room(planlist_html):
    """
    从 planList HTML 中查找目标房型，返回 planRoom ID 列表
    """
    soup = BeautifulSoup(planlist_html, "html.parser")

    matched = []

    for dl in soup.select("dl.plan_room"):
        # 提取房型名称
        title_el = dl.select_one("dt span")
        if not title_el:
            continue

        room_name = title_el.get_text(strip=True)

        # 是否匹配目标房型
        if all(k in room_name for k in TARGET_ROOM_KEYWORDS):
            # 从 class 中提取 planRoom ID
            classes = dl.get("class", [])
            for cls in classes:
                m = re.match(r"planRoom_(\d+)", cls)
                if m:
                    plan_room_id = m.group(1)
                    matched.append({
                        "planRoomId": plan_room_id,
                        "roomName": room_name
                    })

    return matched


def main():
    print("🔍 请求 planlist/search ...")
    html = fetch_planlist_html()

    if not html.strip():
        print("❌ 未返回任何 planList HTML，可能参数不对或当天无房")
        return

    print("🔎 解析房型信息 ...")
    results = find_target_plan_room(html)

    if not results:
        print("❌ 未找到「庭園露天風呂付和室80平米」")
    else:
        print("✅ 找到目标房型：")
        for r in results:
            print(f"  - planRoomId: {r['planRoomId']}")
            print(f"    roomName:   {r['roomName']}")


def check_target_room_found(date):
    """ 检查目标房型是否找到，返回 True/False """
    html = fetch_planlist_html(date)
    if not html.strip():
        return False
    results = find_target_plan_room(html)
    return len(results) > 0


if __name__ == "__main__":
    main()
