import sys

def add_profile_dropdown(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add CSS for the Dropdown
    dropdown_css = """
    /* ── PROFILE DROPDOWN STYLES ── */
    .profile-container {
      position: relative;
      display: inline-block;
    }
    .profile-trigger {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 15px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-light);
      border-radius: 50px;
      cursor: pointer;
      transition: all 0.3s;
      box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .profile-trigger:hover {
      background: #fff;
      box-shadow: 0 8px 25px var(--glow-pink);
      transform: translateY(-2px);
    }
    .profile-img {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--pink-deep), var(--blue-deep));
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-size: 0.8rem;
    }
    .profile-name {
      font-weight: 800;
      font-size: 0.85rem;
      color: var(--text-primary);
    }

    .dropdown-menu {
      position: absolute;
      top: calc(100% + 12px);
      right: 0;
      width: 220px;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(20px);
      border: 1.5px solid var(--border-light);
      border-radius: 24px;
      padding: 12px;
      box-shadow: 0 15px 40px rgba(0,0,0,0.1);
      display: none;
      flex-direction: column;
      gap: 5px;
      z-index: 5000;
      transform-origin: top right;
      animation: dropdownSlide 0.3s cubic-bezier(0.18, 0.89, 0.32, 1.28);
    }
    .dropdown-menu.show {
      display: flex;
    }
    @keyframes dropdownSlide {
      from { opacity: 0; transform: scale(0.9) translateY(-10px); }
      to { opacity: 1; transform: scale(1) translateY(0); }
    }
    .dropdown-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 16px;
      border-radius: 14px;
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 0.2s;
    }
    .dropdown-item:hover {
      background: var(--bg-primary);
      color: var(--pink-deep);
      padding-left: 20px;
    }
    .dropdown-item.logout {
      color: #ff7e7e;
      margin-top: 5px;
      border-top: 1.5px solid var(--border-light);
      padding-top: 15px;
      border-radius: 0 0 14px 14px;
    }
    .dropdown-item.logout:hover {
      background: rgba(255, 126, 126, 0.1);
      color: #ff5e5e;
    }
    """
    if '</style>' in content:
        content = content.replace('</style>', dropdown_css + '</style>')

    # 2. Update Header HTML
    # First, remove the old logout button and profile icon
    old_logout = '<button class="btn btn-outline" style="padding: 10px 20px; margin-left: 20px; font-size: 0.85rem; background: #ff7e7e; color: #fff; border: none; border-radius: 12px; font-weight: 800; cursor: pointer; box-shadow: 0 4px 12px rgba(255,126,126,0.3);" onclick="logout()">🚪 Logout</button>'
    old_profile = '<div class="profile-icon" onclick="openProfileModal()">⋮</div>'
    
    content = content.replace(old_logout, '')
    
    new_dropdown_html = """
    <div class="profile-container" id="profile-dropdown-container">
      <div class="profile-trigger" onclick="toggleDropdown(event)">
        <div class="profile-img">👤</div>
        <div class="profile-name">Dedicated Learner</div>
      </div>
      <div class="dropdown-menu" id="profile-dropdown">
        <div class="dropdown-item" onclick="openProfileModal()">
          <span>👤</span> Profile & Bio
        </div>
        <div class="dropdown-item" onclick="alert('Daily tasks sync coming soon!')">
          <span>📝</span> Edit Daily Tasks
        </div>
        <div class="dropdown-item" onclick="openProfileModal()">
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
    
    if old_profile in content:
        content = content.replace(old_profile, new_dropdown_html)

    # 3. Add Dropdown Toggle JS
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
    """
    if '  </script>' in content:
        content = content.replace('  </script>', dropdown_js + '  </script>')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

add_profile_dropdown('study_timetable.html')
add_profile_dropdown('index.html')
print("Added Premium Profile Dropdown to both files.")
