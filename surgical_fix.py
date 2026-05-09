import sys

def final_manual_dropdown_fix(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Define the new Dropdown HTML
    dropdown_html = """
    <div class="profile-container" id="profile-dropdown-container">
      <div class="profile-trigger" onclick="toggleDropdown(event)">
        <div class="profile-img">👤</div>
        <div class="profile-name">Dedicated Learner</div>
      </div>
      <div class="dropdown-menu" id="profile-dropdown">
        <div class="dropdown-item" onclick="toggleProfileModal()">
          <span>👤</span> Profile & Bio
        </div>
        <div class="dropdown-item" onclick="alert('Daily tasks sync coming soon!')">
          <span>📝</span> Edit Daily Tasks
        </div>
        <div class="dropdown-item" onclick="toggleProfileModal()">
          <span>📊</span> Performance Stats
        </div>
        <div class="dropdown-item" onclick="resetAll()">
          <span>🔄</span> Reset Progress
        </div>
        <div class="dropdown-item logout" onclick="logout()">
          <span>🚪</span> Logout
        </div>
      </div>
    </div>
    """

    # 2. Replace the old profile-btn
    target_btn = '<button id="profile-btn" onclick="toggleProfileModal()" title="Profile & Stats">\n      ⋮\n    </button>'
    if target_btn in content:
        content = content.replace(target_btn, dropdown_html)
    else:
        # Try a more loose match
        import re
        content = re.sub(r'<button id="profile-btn".*?>\s*⋮\s*</button>', dropdown_html, content, flags=re.DOTALL)

    # 3. Add JS functions if missing
    dropdown_js = """
    function toggleDropdown(event) {
      event.stopPropagation();
      document.getElementById('profile-dropdown').classList.toggle('show');
    }

    window.addEventListener('click', () => {
      const dropdown = document.getElementById('profile-dropdown');
      if (dropdown && dropdown.classList.contains('show')) {
        dropdown.classList.remove('show');
      }
    });

    function logout() {
      if (typeof auth !== 'undefined') {
        auth.signOut().then(() => {
          location.reload();
        });
      } else {
        localStorage.removeItem('study_current_user');
        location.reload();
      }
    }
    """
    if '  </script>' in content and 'toggleDropdown' not in content:
        content = content.replace('  </script>', dropdown_js + '  </script>')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

final_manual_dropdown_fix('study_timetable.html')
final_manual_dropdown_fix('index.html')
print("Successfully applied the final manual fix for the Profile Dropdown.")
