import sys

def sync_auth_to_index(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add Firebase SDKs if missing
    firebase_scripts = """
  <!-- Firebase SDKs -->
  <script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-auth-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore-compat.js"></script>
    """
    if '</head>' in content and 'firebase-app-compat.js' not in content:
        content = content.replace('</head>', firebase_scripts + '</head>')

    # 2. Add Auth CSS if missing
    auth_css = """
    /* ── AUTH SYSTEM STYLES ── */
    #auth-overlay {
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: var(--bg-primary);
      z-index: 20000;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: opacity 0.5s ease-out;
    }
    #auth-overlay.hidden {
      opacity: 0;
      pointer-events: none;
    }
    .auth-card {
      background: var(--bg-card);
      backdrop-filter: blur(24px);
      border: 1.5px solid var(--border-light);
      border-radius: 32px;
      padding: 40px;
      width: 90%;
      max-width: 420px;
      box-shadow: 0 15px 50px rgba(224, 104, 154, 0.2);
      text-align: center;
    }
    .auth-header h2 {
      font-size: 1.8rem;
      font-weight: 900;
      background: linear-gradient(135deg, var(--pink-deep), var(--blue-deep));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 10px;
    }
    .auth-inputs {
      display: flex;
      flex-direction: column;
      gap: 15px;
      margin-top: 25px;
    }
    .auth-input-group {
      text-align: left;
    }
    .auth-input-group label {
      display: block;
      font-size: 0.75rem;
      font-weight: 800;
      color: var(--text-secondary);
      margin-bottom: 6px;
      margin-left: 12px;
    }
    .auth-inputs input {
      width: 100%;
      padding: 14px 20px;
      border-radius: 16px;
      border: 1.5px solid var(--border-light);
      background: rgba(255, 255, 255, 0.5);
      font-family: 'Nunito', sans-serif;
      font-size: 0.9rem;
      color: var(--text-primary);
      outline: none;
      transition: all 0.3s;
    }
    .auth-inputs input:focus {
      border-color: var(--pink-mid);
      box-shadow: 0 0 15px var(--glow-pink);
      background: #fff;
    }
    .auth-btn {
      width: 100%;
      padding: 15px;
      margin-top: 20px;
      border-radius: 16px;
      border: none;
      background: linear-gradient(135deg, var(--pink-deep), var(--blue-deep));
      color: #fff;
      font-weight: 800;
      font-size: 1rem;
      cursor: pointer;
      box-shadow: 0 8px 20px var(--glow-pink);
      transition: all 0.3s;
    }
    .auth-footer {
      margin-top: 20px;
      font-size: 0.85rem;
      color: var(--text-muted);
    }
    .auth-toggle {
      color: var(--pink-deep);
      font-weight: 800;
      cursor: pointer;
      text-decoration: underline;
    }
    """
    if '</style>' in content and 'auth-overlay' not in content:
        content = content.replace('</style>', auth_css + '</style>')

    # 3. Add Auth HTML if missing
    auth_html = """
  <!-- AUTH OVERLAY -->
  <div id="auth-overlay">
    <div class="auth-card">
      <div class="auth-header">
        <h2 id="auth-title">Welcome Back!</h2>
        <p id="auth-subtitle" style="font-size:0.85rem; color:var(--text-muted);">Please login to your study portal</p>
      </div>
      <div class="auth-inputs">
        <div class="auth-input-group">
          <label>EMAIL / USERNAME</label>
          <input type="text" id="username" placeholder="e.g. naveen@study.com">
        </div>
        <div class="auth-input-group">
          <label>PASSWORD</label>
          <input type="password" id="password" placeholder="••••••••">
        </div>
        <button class="auth-btn" id="auth-submit-btn" onclick="handleAuth()">Login Now</button>
      </div>
      <div class="auth-footer">
        <span id="auth-footer-text">Don't have an account?</span> 
        <span class="auth-toggle" onclick="toggleAuthMode()" id="auth-toggle-btn">Create Account</span>
      </div>
    </div>
  </div>
    """
    if '<body>' in content and 'auth-overlay' not in content:
        content = content.replace('<body>', '<body>' + auth_html)

    # 4. Add Firebase Logic
    firebase_logic = """
    // ──────────────────────────────────────────────
    // FIREBASE CLOUD AUTHENTICATION
    // ──────────────────────────────────────────────
    const firebaseConfig = {
      apiKey: "AIzaSyDmajJFBxaIMhjtxL3ESC0g3JxqY3BbaGw",
      authDomain: "studyplan-a2713.firebaseapp.com",
      projectId: "studyplan-a2713",
      storageBucket: "studyplan-a2713.firebasestorage.app",
      messagingSenderId: "384418102724",
      appId: "1:384418102724:web:0d54c31a605fb0c0b03891"
    };

    if (typeof firebase !== 'undefined') {
        firebase.initializeApp(firebaseConfig);
        var auth = firebase.auth();
    }

    let isLoginMode = true;

    function toggleAuthMode() {
      isLoginMode = !isLoginMode;
      document.getElementById('auth-title').innerText = isLoginMode ? "Welcome Back!" : "Join the Journey";
      document.getElementById('auth-submit-btn').innerText = isLoginMode ? "Login Now" : "Create Account";
      document.getElementById('auth-toggle-btn').innerText = isLoginMode ? "Create Account" : "Login Now";
    }

    function handleAuth() {
      const email = document.getElementById('username').value.trim();
      const pass = document.getElementById('password').value.trim();
      if (!email || !pass) return;

      const loginEmail = email.includes('@') ? email : `${email}@study.com`;

      if (isLoginMode) {
        auth.signInWithEmailAndPassword(loginEmail, pass).catch(e => alert(e.message));
      } else {
        auth.createUserWithEmailAndPassword(loginEmail, pass).catch(e => alert(e.message));
      }
    }

    function enterApp() {
      document.getElementById('auth-overlay').classList.add('hidden');
    }

    if (typeof auth !== 'undefined') {
        auth.onAuthStateChanged((user) => {
          if (user) enterApp();
          else document.getElementById('auth-overlay').classList.remove('hidden');
        });
    }
"""
    if '  </script>' in content and 'FIREBASE CLOUD' not in content:
        content = content.replace('  </script>', firebase_logic + '  </script>')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

sync_auth_to_index('index.html')
print("Successfully synced complete Auth System to index.html.")
