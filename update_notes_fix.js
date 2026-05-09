const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const lines = html.split('\n');
let newLines = [];
let i = 0;
let replaced = false;

while(i < lines.length) {
    if (!replaced && lines[i].includes('card.appendChild(body);')) {
        newLines.push(`        const notesDiv = document.createElement('div');
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
        body.appendChild(notesDiv);`);
        
        newLines.push(lines[i]);
        replaced = true;
    } else {
        newLines.push(lines[i]);
    }
    i++;
}

fs.writeFileSync('index.html', newLines.join('\n'));
console.log('Update notes fix successful');
