import sys

def move_logout_button(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove old logout button from modal
    old_btn = '<button class="auth-btn" style="background:#ff7e7e; margin-top:20px;" onclick="logout()">🚪 Logout</button>'
    content = content.replace(old_btn, '')

    # 2. Add new logout button to header-right
    target = '<div class="profile-icon" onclick="openProfileModal()">⋮</div>'
    new_header_btns = '<button class="btn btn-outline" style="padding: 8px 15px; margin-right: 10px; font-size: 0.8rem; background: rgba(255,126,126,0.1); border-color: rgba(255,126,126,0.3); color: #ff7e7e;" onclick="logout()">🚪 Logout</button>\n      ' + target
    
    if target in content and 'onclick="logout()"' not in content:
        content = content.replace(target, new_header_btns)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

move_logout_button('study_timetable.html')
move_logout_button('index.html')
print("Moved Logout button to header.")
