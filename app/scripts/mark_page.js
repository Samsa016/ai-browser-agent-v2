(function() {

    document.querySelectorAll('.ai-mark-container').forEach(el => el.remove());
    
    window.aiElements = [];
    const elements = document.querySelectorAll('button, a, input, textarea, select, [role="button"]');
    
    let count = 0;
    const items = [];

    elements.forEach((el) => {
        const rect = el.getBoundingClientRect();
        if (rect.width < 10 || rect.height < 10 || rect.top < 0) return;
        
        const style = window.getComputedStyle(el);
        if (style.visibility === 'hidden' || style.display === 'none') return;

        const mark = document.createElement('div');
        mark.className = 'ai-mark-container';
        mark.style.position = 'absolute';
        mark.style.left = window.scrollX + rect.left + 'px';
        mark.style.top = window.scrollY + rect.top + 'px';
        mark.style.width = rect.width + 'px';
        mark.style.height = rect.height + 'px';
        mark.style.border = '2px solid red';
        mark.style.zIndex = '999999';
        mark.style.pointerEvents = 'none'; 
        
        const label = document.createElement('div');
        label.innerText = count;
        label.style.position = 'absolute';
        label.style.top = '-15px';
        label.style.left = '0';
        label.style.background = 'red';
        label.style.color = 'white';
        label.style.fontSize = '12px';
        label.style.padding = '2px';
        label.style.fontWeight = 'bold';
        
        mark.appendChild(label);
        document.body.appendChild(mark);

        items.push(el);
        count++;
    });
    window.aiElements = items;
    
    return count;
})();