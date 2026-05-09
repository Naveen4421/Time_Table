import sys

def move_logout_to_left(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove from Right
    right_btn = '<button class="btn btn-outline" style="padding: 10px 20px; margin-right: 15px; font-size: 0.85rem; background: #ff7e7e; color: #fff; border: none; border-radius: 12px; font-weight: 800; cursor: pointer; box-shadow: 0 4px 12px rgba(255,126,126,0.3);" onclick="logout()">🚪 Logout</button>\n      '
    content = content.replace(right_btn, '')

    # 2. Add to Left (next to logo)
    target_left = '<div class="logo">🚀 100-Day Study Plan</div>'
    new_left = target_left + '\n    <button class="btn btn-outline" style="padding: 10px 20px; margin-left: 20px; font-size: 0.85rem; background: #ff7e7e; color: #fff; border: none; border-radius: 12px; font-weight: 800; cursor: pointer; box-shadow: 0 4px 12px rgba(255,126,126,0.3);" onclick="logout()">🚪 Logout</button>'
    
    if target_left in content and 'onclick="logout()"' not in content:
        content = content.replace(target_left, new_left)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

move_logout_to_left('study_timetable.html')
move_logout_to_left('index.html')
print("Moved Logout button to the left side.")
