import sys

def refine_dropdown_and_edit(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove Emojis and Fix HTML
    # Remove from trigger
    content = content.replace('<div class="profile-img">👤</div>', '<div class="profile-img">P</div>')
    
    # Remove from dropdown items
    content = content.replace('<span>👤</span> Profile & Bio', 'Profile & Bio')
    content = content.replace('<span>📝</span> Edit Daily Tasks', 'Edit Daily Tasks')
    content = content.replace('<span>📊</span> Performance Stats', 'Performance Stats')
    content = content.replace('<span>🔄</span> Reset Progress', 'Reset Progress')
    content = content.replace('<span>🚪</span> Logout', 'Logout')

    # 2. Add Edit Mode Styling
    edit_css = """
    .editing-active .session-desc {
      background: rgba(224, 104, 154, 0.1);
      border-radius: 8px;
      padding: 5px;
      cursor: text;
      border: 1px dashed var(--pink-deep);
    }
    """
    if '</style>' in content and '.editing-active' not in content:
        content = content.replace('</style>', edit_css + '</style>')

    # 3. Add Edit Logic and Fix Logout
    edit_js = """
    let editMode = false;
    function editTasks() {
      editMode = !editMode;
      if (editMode) {
        document.body.classList.add('editing-active');
        document.querySelectorAll('.session-desc').forEach(el => {
          el.contentEditable = true;
        });
        alert("Edit Mode ON: You can now click any task text to change it!");
      } else {
        document.body.classList.remove('editing-active');
        document.querySelectorAll('.session-desc').forEach(el => {
          el.contentEditable = false;
          // Save custom names
          const dayId = el.closest('.day-card').dataset.day;
          const sessionId = el.closest('.session-row').dataset.session;
          saveCustomTask(dayId, sessionId, el.innerText);
        });
        alert("Changes Saved!");
      }
    }

    function saveCustomTask(day, session, text) {
      let custom = JSON.parse(localStorage.getItem('custom_study_tasks') || '{}');
      if (!custom[day]) custom[day] = {};
      custom[day][session] = text;
      localStorage.setItem('custom_study_tasks', JSON.stringify(custom));
    }

    // Fix Logout to be more aggressive
    function logout() {
      console.log("Logout triggered");
      if (window.firebase && firebase.auth) {
        firebase.auth().signOut().then(() => {
          window.location.reload(true);
        }).catch(err => {
          console.error(err);
          localStorage.removeItem('study_current_user');
          window.location.reload(true);
        });
      } else {
        localStorage.removeItem('study_current_user');
        window.location.reload(true);
      }
    }
    """
    
    # Update the Edit button in the HTML
    content = content.replace("alert('Daily tasks sync coming soon!')", "editTasks()")
    
    if '  </script>' in content:
        content = content.replace('  </script>', edit_js + '  </script>')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

refine_dropdown_and_edit('study_timetable.html')
refine_dropdown_and_edit('index.html')
print("Cleaned up UI, fixed logout, and enabled Task Editing.")
