const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const icsFunctions = `
    function parseTimeStr(baseDate, timeStr) {
      const parts = timeStr.match(/(\\d+):(\\d+)\\s*(AM|PM)/i);
      if (!parts) return new Date(baseDate);
      let hours = parseInt(parts[1], 10);
      const mins = parseInt(parts[2], 10);
      const ampm = parts[3].toUpperCase();
      if (ampm === 'PM' && hours < 12) hours += 12;
      if (ampm === 'AM' && hours === 12) hours = 0;
      const d = new Date(baseDate);
      d.setHours(hours, mins, 0, 0);
      return d;
    }

    function formatDateICS(date) {
      return date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
    }

    function exportDayToICS(dayIndex) {
      const day = days[dayIndex];
      let icsData = "BEGIN:VCALENDAR\\r\\nVERSION:2.0\\r\\nPRODID:-//TimeTable//EN\\r\\n";

      day.sessions.forEach(sess => {
         if (sess.sub === 'Break') return;
         if (sess.checked) return; // Skip completed
         
         const startTime = parseTimeStr(day.date, sess.start);
         const endTime = parseTimeStr(day.date, sess.end);

         const dtstart = formatDateICS(startTime);
         const dtend = formatDateICS(endTime);
         
         icsData += "BEGIN:VEVENT\\r\\n";
         icsData += \`UID:\${dayIndex}-\${sess.sub.replace(/\\s/g, '')}-\${Date.now()}@timetable\\r\\n\`;
         icsData += \`DTSTAMP:\${formatDateICS(new Date())}\\r\\n\`;
         icsData += \`DTSTART:\${dtstart}\\r\\n\`;
         icsData += \`DTEND:\${dtend}\\r\\n\`;
         icsData += \`SUMMARY:\${sess.sub} - Study Session\\r\\n\`;
         icsData += \`DESCRIPTION:Topic to cover: \${sess.topic}. You got this!\\r\\n\`;
         
         // 30-minute alarm reminder
         icsData += "BEGIN:VALARM\\r\\nTRIGGER:-PT30M\\r\\nACTION:DISPLAY\\r\\nDESCRIPTION:Study Reminder\\r\\nEND:VALARM\\r\\n";
         
         icsData += "END:VEVENT\\r\\n";
      });

      icsData += "END:VCALENDAR\\r\\n";
      
      const blob = new Blob([icsData], { type: 'text/calendar;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = \`Study_Day_\${day.day}.ics\`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      alert("Calendar file downloaded! Click it to instantly add all your study tasks for this day (with 30-min reminders) into Google Calendar!");
    }
  </script>`;

html = html.replace('</script>', icsFunctions);

const lines = html.split('\n');
let newLines = [];
let i = 0;
let replaced = false;

while(i < lines.length) {
    if (!replaced && lines[i].includes('body.appendChild(notesDiv);')) {
        newLines.push(lines[i]);
        
        newLines.push(`        const calBtnDiv = document.createElement('div');
        calBtnDiv.style.marginTop = '15px';
        calBtnDiv.style.display = 'flex';
        calBtnDiv.style.justifyContent = 'flex-end';
        
        const calBtn = document.createElement('button');
        calBtn.innerHTML = '📅 Add to Google Calendar';
        calBtn.style.background = 'var(--pink-pale)';
        calBtn.style.color = 'var(--pink-deep)';
        calBtn.style.border = '1px solid var(--pink-mid)';
        calBtn.style.padding = '8px 14px';
        calBtn.style.borderRadius = '50px';
        calBtn.style.fontSize = '0.75rem';
        calBtn.style.fontWeight = 'bold';
        calBtn.style.cursor = 'pointer';
        calBtn.style.boxShadow = '0 2px 10px rgba(224, 104, 154, 0.15)';
        calBtn.style.transition = 'all 0.2s';
        calBtn.onmouseover = () => calBtn.style.transform = 'scale(1.05)';
        calBtn.onmouseout = () => calBtn.style.transform = 'scale(1)';
        
        calBtn.onclick = () => exportDayToICS(di);
        
        calBtnDiv.appendChild(calBtn);
        body.appendChild(calBtnDiv);`);
        
        replaced = true;
    } else {
        newLines.push(lines[i]);
    }
    i++;
}

fs.writeFileSync('index.html', newLines.join('\n'));
console.log('Update calendar integration successful');
