import sys

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add EmailJS Script Tag
    if '</head>' in content and 'emailjs.browser' not in content:
        content = content.replace('</head>', '<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>\n</head>')

    # Add Buttons and Email Input
    target_btn = '<button class="btn btn-danger" onclick="resetAll()">🗑 Reset All</button>'
    if target_btn in content and 'notify-btn' not in content:
        new_btns = target_btn + """
      <button class="btn btn-primary" id="notify-btn" onclick="requestNotificationPermission()">🔔 Enable Alerts</button>
      <button class="btn btn-outline" onclick="testNotificationSystem()">🧪 Test Alert</button>
      <div style="display:flex; align-items:center; gap:10px; background:var(--bg-glass); padding:5px 15px; border-radius:12px; border:1.5px solid var(--border-light);">
        <span style="font-size:0.8rem; font-weight:800; color:var(--text-secondary);">📧 Alert Email:</span>
        <input type="email" id="alert-email" placeholder="your@email.com" style="border:none; background:transparent; font-family:'Nunito'; font-size:0.8rem; outline:none; color:var(--text-primary); width:150px;">
      </div>"""
        content = content.replace(target_btn, new_btns)

    # Add JS Logic
    js_end = '  </script>'
    if js_end in content and 'sendEmailNotification' not in content:
        js_logic = """
    // ──────────────────────────────────────────────
    // NOTIFICATIONS & EMAIL
    // ──────────────────────────────────────────────
    (function() {
        // Init EmailJS with your key
        if (typeof emailjs !== 'undefined') {
            emailjs.init("bwtmz4IBfxHEZ8SFr");
        }
    })();

    let notifiedSessions = new Set();

    function requestNotificationPermission() {
      if (!("Notification" in window)) {
        alert("This browser does not support desktop notifications.");
        return;
      }
      Notification.requestPermission().then(permission => {
        if (permission === "granted") {
          alert("Notifications enabled! We'll remind you 15 and 5 minutes before each session ends.");
          const btn = document.getElementById('notify-btn');
          if (btn) btn.style.display = 'none';
          checkNotifications();
        }
      });
    }

    function sendEmailNotification(subject, topic, timeRemaining) {
        const userEmail = document.getElementById('alert-email').value;
        if (!userEmail || typeof emailjs === 'undefined') return;

        const templateParams = {
            to_email: userEmail,
            subject_name: subject,
            topic_name: topic,
            time_left: timeRemaining,
            message: `Your ${subject} session is ending in ${timeRemaining} minutes. Topic covered: ${topic}`
        };

        // service_640rl8n is your Service ID
        // Replace 'YOUR_TEMPLATE_ID' once you have it!
        emailjs.send('service_640rl8n', 'YOUR_TEMPLATE_ID', templateParams)
            .then(function(response) {
               console.log('Email sent successfully!', response.status, response.text);
            }, function(error) {
               console.log('Email failed...', error);
            });
    }

    function checkNotifications() {
      if (Notification.permission !== "granted") return;

      const now = new Date();
      const todayIdx = days.findIndex(d => d.date.toDateString() === now.toDateString());
      if (todayIdx === -1) return;

      const today = days[todayIdx];
      
      today.sessions.forEach((sess, si) => {
        if (sess.sub === 'Break') return;
        
        const endTime = parseTimeStr(now, sess.end);
        const timeDiff = (endTime - now) / (1000 * 60);
        const remaining = Math.round(timeDiff);
        const intervals = [15, 5];
        
        intervals.forEach(interval => {
            const sessionKey = `${todayIdx}-${si}-${interval}`;
            if (remaining === interval && !notifiedSessions.has(sessionKey)) {
              sendEmailNotification(sess.sub, sess.topic, interval);
              new Notification(`${interval} Minutes Remaining!`, {
                body: `Your ${sess.sub} session ends in ${interval} minutes. Finish: ${sess.topic}`,
                icon: "https://cdn-icons-png.flaticon.com/512/3208/3208615.png"
              });
              notifiedSessions.add(sessionKey);
            }
        });
      });
    }

    function testNotificationSystem() {
        if (!document.getElementById('alert-email').value) {
            alert("Please enter an email first!");
            return;
        }
        new Notification("Test Success!", {
            body: "If you see this, your browser pop-ups are working! Now check your email.",
            icon: "https://cdn-icons-png.flaticon.com/512/3208/3208615.png"
        });
        sendEmailNotification("TEST SUBJECT", "Testing Topic", 99);
        alert("Test triggered! Check your desktop and your email inbox.");
    }

    setInterval(checkNotifications, 60000);
"""
        content = content.replace(js_end, js_logic + js_end)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

update_file('study_timetable.html')
print("Successfully updated study_timetable.html with all notification features.")
