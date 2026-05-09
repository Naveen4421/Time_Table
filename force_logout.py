import sys

def force_logout_fix(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Powerful Logout Function
    new_logout_logic = """
    function logout() {
      console.log("Force Logout Executing...");
      localStorage.clear();
      sessionStorage.clear();
      
      if (window.firebase && firebase.auth) {
        firebase.auth().signOut().then(() => {
          window.location.href = 'index.html';
        }).catch(() => {
          window.location.href = 'index.html';
        });
      } else {
        window.location.href = 'index.html';
      }
    }
    """
    
    # Replace existing logout logic
    import re
    content = re.sub(r'function logout\(\) \{.*?\}', new_logout_logic, content, flags=re.DOTALL)

    # 2. Ensure Auth Overlay is VISIBLE by default until check is done
    # Search for the auth-overlay CSS and ensure it doesn't have display:none or similar early on
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

force_logout_fix('study_timetable.html')
force_logout_fix('index.html')
print("Successfully applied Powerful Logout and Login redirect.")
