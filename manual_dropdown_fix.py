import sys

def manual_fix_dropdown(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    found = False
    for line in lines:
        # Look for the profile-icon div and replace it
        if 'class="profile-icon"' in line and 'onclick="openProfileModal()"' in line:
            indent = line[:line.find('<')]
            dropdown_html = f"""{indent}<div class="profile-container" id="profile-dropdown-container">
{indent}  <div class="profile-trigger" onclick="toggleDropdown(event)">
{indent}    <div class="profile-img">👤</div>
{indent}    <div class="profile-name">Dedicated Learner</div>
{indent}  </div>
{indent}  <div class="dropdown-menu" id="profile-dropdown">
{indent}    <div class="dropdown-item" onclick="openProfileModal()">
{indent}      <span>👤</span> Profile & Bio
{indent}    </div>
{indent}    <div class="dropdown-item" onclick="alert('Daily tasks sync coming soon!')">
{indent}      <span>📝</span> Edit Daily Tasks
{indent}    </div>
{indent}    <div class="dropdown-item" onclick="openProfileModal()">
{indent}      <span>📊</span> Performance Stats
{indent}    </div>
{indent}    <div class="dropdown-item" onclick="resetAll()">
{indent}      <span>🔄</span> Reset Progress
{indent}    </div>
{indent}    <div class="dropdown-item logout" onclick="logout()">
{indent}      <span>🚪</span> Logout
{indent}    </div>
{indent}  </div>
{indent}</div>\n"""
            new_lines.append(dropdown_html)
            found = True
        elif 'onclick="logout()"' in line and 'button' in line:
            # Skip old logout button if it was added separately
            continue
        else:
            new_lines.append(line)

    if found:
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

manual_fix_dropdown('study_timetable.html')
manual_fix_dropdown('index.html')
print("Manually fixed the Profile Dropdown UI.")
