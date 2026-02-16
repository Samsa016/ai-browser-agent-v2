(function() {
    document.querySelectorAll('.ai-mark-container').forEach(el => el.remove());
    window.aiElements = [];

    const selectors = [
        'input:not([type="hidden"])', 
        'textarea', 
        'select', 
        'button', 
        'a[href]', 
        '[role="button"]', 
        '[onclick]'
    ].join(',');

    const elements = document.querySelectorAll(selectors);
    
    let count = 0;
    const items = [];

    elements.forEach((el) => {
        const rect = el.getBoundingClientRect();
        
        if (rect.width < 15 || rect.height < 15) return;
        
        const style = window.getComputedStyle(el);
        if (style.visibility === 'hidden' || style.display === 'none' || style.opacity === '0') return;
        
        const mark = document.createElement('div');
        mark.className = 'ai-mark-container';
        mark.style.position = 'absolute';
        mark.style.left = (window.scrollX + rect.left) + 'px';
        mark.style.top = (window.scrollY + rect.top) + 'px';
        mark.style.width = rect.width + 'px';
        mark.style.height = rect.height + 'px';
        mark.style.zIndex = '2147483647'; 
        mark.style.pointerEvents = 'none'; 
        
        let isInput = el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT';
        
        const color = isInput ? 'blue' : 'red';
        mark.style.border = `2px solid ${color}`;
        

        const label = document.createElement('div');
        label.innerText = count;
        label.style.position = 'absolute';
        label.style.top = '-19px';
        label.style.right = '0'; 
        label.style.background = color;
        label.style.color = 'white';
        label.style.fontSize = '14px';
        label.style.fontWeight = 'bold';
        label.style.padding = '2px 5px';
        label.style.borderRadius = '3px';
        
        mark.appendChild(label);
        document.body.appendChild(mark);

        items.push(el);
        count++;
    });

    window.aiElements = items;
    return count;
})();