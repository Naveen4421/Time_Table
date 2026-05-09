const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const cssInjection = `
    .top-controls {
      position: fixed;
      top: 18px;
      right: 22px;
      z-index: 9999;
      display: flex;
      gap: 10px;
    }
    
    #profile-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 42px;
      height: 42px;
      border-radius: 50%;
      border: 1.5px solid rgba(224, 104, 154, 0.35);
      background: rgba(255, 255, 255, 0.75);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      cursor: pointer;
      font-size: 1.2rem;
      font-weight: 800;
      color: #7a5271;
      box-shadow: 0 4px 18px rgba(224, 104, 154, 0.18);
      transition: all 0.3s;
    }
    #profile-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 7px 24px rgba(224, 104, 154, 0.28);
    }
    [data-theme="dark"] #profile-btn {
      border-color: rgba(200, 200, 200, 0.2);
      background: rgba(28, 28, 28, 0.85);
      color: #c8c8c8;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4);
    }
    [data-theme="dark"] #profile-btn:hover {
      box-shadow: 0 7px 24px rgba(0, 0, 0, 0.55);
    }

    /* Modal Styles */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.4);
      backdrop-filter: blur(4px);
      z-index: 10000;
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s;
    }
    .modal-overlay.active {
      opacity: 1;
      pointer-events: all;
    }
    .profile-modal {
      background: var(--bg-primary);
      border: 1.5px solid var(--border-light);
      border-radius: 24px;
      width: 90%;
      max-width: 450px;
      padding: 30px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.15);
      transform: translateY(20px) scale(0.95);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
    }
    .modal-overlay.active .profile-modal {
      transform: translateY(0) scale(1);
    }
    .close-modal {
      position: absolute;
      top: 20px; right: 20px;
      background: transparent; border: none;
      font-size: 1.5rem; color: var(--text-muted);
      cursor: pointer; transition: color 0.2s;
    }
    .close-modal:hover { color: var(--pink-deep); }
    
    .profile-header {
      display: flex; flex-direction: column; align-items: center;
      margin-bottom: 25px;
    }
    .profile-avatar {
      width: 90px; height: 90px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--pink-mid), var(--blue-mid));
      display: flex; align-items: center; justify-content: center;
      font-size: 2.5rem; border: 4px solid var(--bg-card);
      box-shadow: 0 4px 15px var(--glow-pink);
      margin-bottom: 12px;
    }
    .profile-name {
      font-size: 1.4rem; font-weight: 900; color: var(--text-primary);
    }
    .profile-title {
      font-size: 0.9rem; font-weight: 700; color: var(--text-secondary);
      background: var(--bg-glass); padding: 4px 12px; border-radius: 50px; margin-top: 5px;
    }
    
    .perf-chart {
      display: flex; justify-content: space-around; align-items: flex-end;
      height: 140px; background: var(--bg-card);
      border: 1.5px solid var(--border-blue); border-radius: 16px;
      padding: 20px 10px 10px; margin-top: 15px;
    }
    .perf-col {
      display: flex; flex-direction: column; align-items: center; gap: 8px;
    }
    .perf-bar-bg {
      width: 24px; height: 90px; background: var(--pink-blush);
      border-radius: 12px; display: flex; align-items: flex-end;
      overflow: hidden;
    }
    .perf-bar-fill {
      width: 100%; background: linear-gradient(0deg, var(--pink-deep), var(--blue-mid));
      border-radius: 12px; transition: height 0.8s ease-out;
    }
    .perf-label {
      font-size: 0.7rem; font-weight: 800; color: var(--text-muted);
    }
    .perf-pct {
      font-size: 0.65rem; font-weight: 800; color: var(--text-primary);
    }
    
    @media (max-width: 600px) {
      .top-controls {
        top: 12px;
        right: 12px;
      }
      #theme-toggle {
        padding: 7px 12px;
        font-size: 0.73rem;
        position: static !important;
      }
      #profile-btn {
        width: 36px; height: 36px; font-size: 1rem;
      }
    }
  </style>`;

html = html.replace('</style>', cssInjection);

html = html.replace(/#theme-toggle \{\s*position: fixed;\s*top: 18px;\s*right: 22px;\s*z-index: 9999;/g, '#theme-toggle {\n');
html = html.replace(/#theme-toggle \{\s*top: 12px;\s*right: 12px;\s*padding: 7px 12px;\s*font-size: 0.73rem;\s*\}/, '');


const htmlInjection = `  <!-- TOP CONTROLS -->
  <div class="top-controls">
    <button id="theme-toggle" onclick="toggleTheme()" title="Switch theme" style="border: 1.5px solid rgba(224, 104, 154, 0.35); background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); cursor: pointer; border-radius: 50px; font-weight: 800; color: #7a5271; padding: 8px 16px; display: flex; align-items: center; gap: 7px;">
      <span class="toggle-icon" id="toggle-icon">🌙</span>
      <span id="toggle-label">Dark Mode</span>
    </button>
    <button id="profile-btn" onclick="toggleProfileModal()" title="Profile & Stats">
      ⋮
    </button>
  </div>

  <!-- PROFILE MODAL -->
  <div class="modal-overlay" id="profileModal" onclick="if(event.target===this) toggleProfileModal()">
    <div class="profile-modal">
      <button class="close-modal" onclick="toggleProfileModal()">×</button>
      <div class="profile-header">
        <div class="profile-avatar">👨‍💻</div>
        <div class="profile-name">Dedicated Learner</div>
        <div class="profile-title">🎯 Master of the 365-Day Journey</div>
      </div>
      
      <h3 style="font-size:0.95rem; font-weight:800; color:var(--text-secondary); margin-bottom: 5px;">Performance by Topic</h3>
      <div class="perf-chart" id="perfChart">
        <!-- Bars injected here -->
      </div>
    </div>
  </div>`;

const oldBtnRegex = /<!-- 🌙 THEME TOGGLE -->\s*<button id="theme-toggle" onclick="toggleTheme\(\)" title="Switch theme">\s*<span class="toggle-icon" id="toggle-icon">🌙<\/span>\s*<span id="toggle-label">Dark Mode<\/span>\s*<\/button>/;
html = html.replace(oldBtnRegex, htmlInjection);


const jsInjection = `
    function toggleProfileModal() {
      const modal = document.getElementById('profileModal');
      const isActive = modal.classList.contains('active');
      
      if (!isActive) {
        const s = getStats();
        const chart = document.getElementById('perfChart');
        chart.innerHTML = '';
        
        SUBJECTS.forEach(sub => {
          const spct = s.subTotal[sub] > 0 ? Math.round((s.subChecked[sub] || 0) / s.subTotal[sub] * 100) : 0;
          
          let colorClass = 'var(--pink-deep)';
          if(sub==='CN') colorClass = 'var(--cn)';
          else if(sub==='OS') colorClass = 'var(--os)';
          else if(sub==='Aptitude') colorClass = 'var(--apt)';
          else if(sub==='Project') colorClass = 'var(--proj)';

          chart.innerHTML += \`
            <div class="perf-col">
              <span class="perf-pct">\${spct}%</span>
              <div class="perf-bar-bg">
                <div class="perf-bar-fill" style="height: 0%; background: \${colorClass}"></div>
              </div>
              <span class="perf-label">\${sub}</span>
            </div>
          \`;
        });
        
        setTimeout(() => {
          const fills = chart.querySelectorAll('.perf-bar-fill');
          SUBJECTS.forEach((sub, i) => {
            const spct = s.subTotal[sub] > 0 ? Math.round((s.subChecked[sub] || 0) / s.subTotal[sub] * 100) : 0;
            if(fills[i]) fills[i].style.height = spct + '%';
          });
        }, 50);
      }
      
      modal.classList.toggle('active');
    }
  </script>`;
html = html.replace('</script>', jsInjection);

fs.writeFileSync('index.html', html);
console.log('Update successful');
