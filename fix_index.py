import sys

def fix_index_html(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add Logout Button to Header
    target_header = '<div class="profile-icon" onclick="openProfileModal()">⋮</div>'
    logout_btn = '<button class="btn btn-outline" style="padding: 10px 20px; margin-right: 15px; font-size: 0.85rem; background: #ff7e7e; color: #fff; border: none; border-radius: 12px; font-weight: 800; cursor: pointer; box-shadow: 0 4px 12px rgba(255,126,126,0.3);" onclick="logout()">🚪 Logout</button>\n      '
    
    if target_header in content and 'onclick="logout()"' not in content:
        content = content.replace(target_header, logout_btn + target_header)

    # 2. Add Logout Logic
    js_end = '  </script>'
    logout_logic = """
    function logout() {
      // For Firebase
      if (typeof auth !== 'undefined') {
        auth.signOut().then(() => {
          location.reload();
        });
      } else {
        // For localStorage backup
        localStorage.removeItem('study_current_user');
        location.reload();
      }
    }
"""
    if js_end in content and 'function logout()' not in content:
        content = content.replace(js_end, logout_logic + js_end)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

fix_index_html('index.html')
print("Successfully fixed index.html.")
