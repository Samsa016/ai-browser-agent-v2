(function() {
    document.querySelectorAll(".ai-label").forEach(el => el.remove());
    
    window.aiElements = {}; 
    let counter = 0;
    const selector = "button, a, input, textarea, select, [role='button'], [onclick]";
    const elements = document.querySelectorAll(selector);

    elements.forEach(el => {
        const rect = el.getBoundingClientRect();
        
        if (rect.width === 0 || rect.height === 0 || window.getComputedStyle(el).visibility === "hidden") {
            return;
        }

        if (rect.bottom < 0 || rect.top > window.innerHeight || rect.right < 0 || rect.left > window.innerWidth) {
            return; 
        }

        counter++;

        const label = document.createElement("div");
        label.className = "ai-label";
        label.textContent = counter;
        
        Object.assign(label.style, {
            position: "absolute",
            left: (window.scrollX + rect.left) + "px",
            top: (window.scrollY + rect.top) + "px",
            backgroundColor: "#ff0000",
            color: "white",
            padding: "2px 4px",
            fontSize: "12px",
            fontWeight: "bold",
            borderRadius: "2px",
            zIndex: "2147483647",
            pointerEvents: "none"
        });

        document.body.appendChild(label);
        
        window.aiElements[counter] = el;
    });

    return counter;
})();