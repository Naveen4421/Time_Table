const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const cssInjection = `
    .daily-note {
      width: 100%;
      min-height: 60px;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1.5px solid var(--border-light);
      background: var(--bg-glass);
      color: var(--text-primary);
      font-family: 'Nunito', sans-serif;
      font-size: 0.82rem;
      resize: vertical;
      transition: border-color 0.2s, box-shadow 0.2s;
      margin-top: 5px;
    }
    .daily-note:focus {
      outline: none;
      border-color: var(--pink-mid);
      box-shadow: 0 0 10px var(--glow-pink);
    }
    [data-theme="dark"] .daily-note {
      border-color: #333;
      background: rgba(22, 22, 22, 0.5);
      color: #eee;
    }
    [data-theme="dark"] .daily-note:focus {
      border-color: #666;
      box-shadow: 0 0 10px rgba(255,255,255,0.1);
    }
  </style>`;
html = html.replace('</style>', cssInjection);

html = html.replace(
  /function save\(\) \{\s*const data = days\.map\(d => d\.sessions\.map\(s => s\.checked\)\);\s*localStorage\.setItem\(LS_KEY, JSON\.stringify\(data\)\);\s*\}/,
  `function save() {
      const data = days.map(d => ({
        checks: d.sessions.map(s => s.checked),
        note: d.note || ""
      }));
      localStorage.setItem(LS_KEY, JSON.stringify(data));
    }`
);

const oldLoadRegex = /function load\(\) \{[\s\S]*?catch \(e\) \{ \}\s*\}/m;
const newLoad = `function load() {
      const raw = localStorage.getItem(LS_KEY);
      if (!raw) return;
      try {
        const data = JSON.parse(raw);
        data.forEach((dayData, di) => {
          if (!days[di]) return;
          if (Array.isArray(dayData)) {
            dayData.forEach((checked, si) => {
              if (days[di].sessions[si]) days[di].sessions[si].checked = !!checked;
            });
            days[di].note = "";
          } else {
            if(dayData.checks) {
              dayData.checks.forEach((checked, si) => {
                if (days[di].sessions[si]) days[di].sessions[si].checked = !!checked;
              });
            }
            days[di].note = dayData.note || "";
          }
        });
      } catch (e) { }
    }`;
html = html.replace(oldLoadRegex, newLoad);

const oldAppendRegex = /(body\.appendChild\(row\);\s*\n\s*\});\s*\n\s*card\.appendChild\(body\);/m;
const newAppend = `$1

        const notesDiv = document.createElement('div');
        notesDiv.style.marginTop = '15px';
        notesDiv.style.borderTop = '1.5px dashed var(--border-light)';
        notesDiv.style.paddingTop = '15px';
        
        const noteLabel = document.createElement('div');
        noteLabel.textContent = "📝 Daily Notes & Feedback";
        noteLabel.style.fontSize = '0.8rem';
        noteLabel.style.fontWeight = '800';
        noteLabel.style.color = 'var(--text-secondary)';
        noteLabel.style.marginBottom = '6px';
        
        const noteArea = document.createElement('textarea');
        noteArea.className = 'daily-note';
        noteArea.placeholder = "Write what you learned today, what to revise, or how you felt...";
        noteArea.value = day.note || "";
        noteArea.oninput = (e) => {
          day.note = e.target.value;
          save();
        };
        
        notesDiv.appendChild(noteLabel);
        notesDiv.appendChild(noteArea);
        body.appendChild(notesDiv);

        card.appendChild(body);`;
        
html = html.replace(oldAppendRegex, newAppend);

fs.writeFileSync('index.html', html);
console.log('Update notes successful');
