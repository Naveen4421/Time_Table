const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

html = html.replace(/MISSION 100: STUDY PLAN!!/g, 'YEARLY STUDY PLAN!!');
html = html.replace(/Interactive 100-day/g, 'Interactive yearly');
html = html.replace(/🎯 Mission 100/g, '🎯 Yearly Plan');
html = html.replace(/100-Day Tracker/g, 'Yearly Tracker');
html = html.replace(/100-day journey/g, 'year-long journey');
html = html.replace(/0 \/ 500 sessions completed/g, '0 sessions completed');

html = html.replace(
  /const START_DATE = new Date\(2026, 3, 12\);.*/,
  'const START_DATE = new Date(new Date().getFullYear(), 0, 1);'
);

html = html.replace(
  /function generateDays\(\) \{\s*const days = \[\];\s*for \(let d = 1; d <= 100; d\+\+\) \{/,
  `function generateDays() {
      const days = [];
      const currentYear = START_DATE.getFullYear();
      const isLeapYear = (currentYear % 4 === 0 && currentYear % 100 !== 0) || (currentYear % 400 === 0);
      const totalDays = isLeapYear ? 366 : 365;
      for (let d = 1; d <= totalDays; d++) {`
);

html = html.replace(/Math\.min\(d1 \+ 6, 100\)/g, 'Math.min(d1 + 6, days.length)');
html = html.replace(/Math\.min\(d1 \+ 7, 100\)/g, 'Math.min(d1 + 7, days.length)');
html = html.replace(/< 100/g, '< days.length');
html = html.replace(/for \(let w = 0; w < 15; w\+\+\)/g, 'const totalWeeks = Math.ceil(days.length / 7); for (let w = 0; w < totalWeeks; w++)');

const journeyMapRegex = /function renderJourneyMap\(\) \{[\s\S]*?\}\s*function jumpToDay/m;
const newRenderCalendar = `function renderJourneyMap() {
      const container = document.getElementById('journeyGrid');
      if (!container) return;
      container.innerHTML = '';
      
      const yearStr = START_DATE.getFullYear();
      container.style.display = 'grid';
      container.style.gridTemplateColumns = 'repeat(auto-fit, minmax(220px, 1fr))';
      container.style.gap = '20px';
      container.style.width = '100%';
      container.style.height = 'auto';
      container.style.position = 'relative';
      
      const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
      
      let dayIndex = 0;
      
      for (let m = 0; m < 12; m++) {
        const monthDiv = document.createElement('div');
        monthDiv.className = 'month-block';
        
        const title = document.createElement('h3');
        title.textContent = monthNames[m];
        title.style.marginBottom = '10px';
        title.style.fontSize = '0.9rem';
        title.style.color = 'var(--text-secondary)';
        title.style.textAlign = 'center';
        monthDiv.appendChild(title);
        
        const grid = document.createElement('div');
        grid.style.display = 'grid';
        grid.style.gridTemplateColumns = 'repeat(7, 1fr)';
        grid.style.gap = '4px';
        
        ['S','M','T','W','T','F','S'].forEach(dw => {
          const w = document.createElement('div');
          w.textContent = dw;
          w.style.fontSize = '0.65rem';
          w.style.color = 'var(--text-muted)';
          w.style.textAlign = 'center';
          grid.appendChild(w);
        });
        
        const firstDayOfMonth = new Date(yearStr, m, 1).getDay();
        for(let i = 0; i < firstDayOfMonth; i++) {
          grid.appendChild(document.createElement('div'));
        }
        
        const daysInMonth = new Date(yearStr, m + 1, 0).getDate();
        for(let d = 1; d <= daysInMonth; d++) {
          if (dayIndex >= days.length) break;
          const currentIdx = dayIndex;
          const day = days[currentIdx];
          
          const ss = studySessions(day.sessions);
          const done = ss.filter(s => s.checked).length;
          const pct = ss.length > 0 ? Math.round(done / ss.length * 100) : 0;
          const isComplete = pct === 100 && ss.length > 0;
          
          const today = new Date(); today.setHours(0, 0, 0, 0);
          const dDate = new Date(day.date); dDate.setHours(0, 0, 0, 0);
          const isToday = dDate.getTime() === today.getTime();
          
          const cell = document.createElement('div');
          cell.className = 'cal-node' + (isComplete ? ' completed' : '') + (isToday ? ' today' : '');
          cell.textContent = d;
          
          cell.onclick = () => jumpToDay(currentIdx);
          
          grid.appendChild(cell);
          dayIndex++;
        }
        
        monthDiv.appendChild(grid);
        container.appendChild(monthDiv);
      }
    }

    function jumpToDay`;
html = html.replace(journeyMapRegex, newRenderCalendar);

const oldCssRegex = /\.journey-node \{[\s\S]*?\[data-theme="dark"\] \.journey-node\.today \{[\s\S]*?\}/m;
const newCss = `.cal-node {
      aspect-ratio: 1;
      border-radius: 6px;
      border: 1px solid var(--border-blue);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.7rem;
      font-weight: 700;
      cursor: pointer;
      background: var(--bg-primary);
      color: var(--text-secondary);
      transition: all 0.2s;
    }
    .cal-node:hover {
      transform: scale(1.15);
      border-color: var(--pink-mid);
      box-shadow: 0 4px 12px var(--glow-pink);
      z-index: 2;
    }
    .cal-node.completed {
      background: linear-gradient(135deg, var(--accent-done), #54b489);
      color: #fff;
      border-color: transparent;
    }
    .cal-node.today {
      border-color: var(--pink-deep);
      background: var(--pink-pale);
      color: var(--pink-deep);
      box-shadow: 0 0 0 2px rgba(224, 104, 154, 0.2);
    }
    [data-theme="dark"] .cal-node {
      border-color: #444;
      background: #141414;
      color: #aaa;
    }
    [data-theme="dark"] .cal-node.completed {
      background: linear-gradient(135deg, #6abf8a, #4a996b);
      color: #000;
    }
    [data-theme="dark"] .cal-node.today {
      border-color: #fff;
      background: #333;
      color: #fff;
      box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.2);
    }`;
html = html.replace(oldCssRegex, newCss);

fs.writeFileSync('index.html', html);
console.log('Update successful');
