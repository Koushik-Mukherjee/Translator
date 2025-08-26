const languages = [
    { "code": "en", "name": "English" },
    { "code": "zh", "name": "Chinese (Simplified)" },
    { "code": "es", "name": "Spanish" },
    { "code": "hi", "name": "Hindi" },
    { "code": "ar", "name": "Arabic" },
    { "code": "ru", "name": "Russian" },
    { "code": "de", "name": "German" },
    { "code": "fr", "name": "French" },
    { "code": "ko", "name": "Korean" },
    { "code": "tr", "name": "Turkish" },
    { "code": "it", "name": "Italian" },
    { "code": "nl", "name": "Dutch" }
];

const fromSelect = document.getElementById('fromLang');
const toSelect = document.getElementById('toLang');

window.onload = () => {
    // Populate "To" dropdown
    languages.forEach(lang => {
        const toOption = document.createElement('option');
        toOption.value = lang.code;
        toOption.textContent = lang.name;
        toSelect.appendChild(toOption);
    });

    // Populate "From" dropdown, including the "Auto-detect" option
    const autoOption = document.createElement('option');
    autoOption.value = "auto";
    autoOption.textContent = "Auto-detect";
    fromSelect.appendChild(autoOption);

    languages.forEach(lang => {
        const fromOption = document.createElement('option');
        fromOption.value = lang.code;
        fromOption.textContent = lang.name;
        fromSelect.appendChild(fromOption);
    });
    
    // Set default selections
    fromSelect.value = 'auto'; 
    toSelect.value = 'de'; // Default to German
};

async function translateText() {
    const inputText = document.getElementById("inputText").value.trim();
    const fromLang = document.getElementById("fromLang").value;
    const toLang = document.getElementById("toLang").value;
    const outputDiv = document.getElementById("outputText");

    if (!inputText) {
        outputDiv.innerText = "⚠️ Please enter text to translate.";
        return;
    }

    outputDiv.innerText = "⏳ Translating...";

    const payload = {
        text: inputText,
        target_language: toLang,
    };

    if (fromLang !== "auto") {
        payload.source_language = fromLang;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/translate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        
        if (data.error) {
             outputDiv.innerText = "❌ Error: " + data.error;
        } else {
             outputDiv.innerText = data.translated_text;
        }
    } catch (error) {
        outputDiv.innerText = "🚨 Failed to connect to server. Is it running?";
        console.error("Translation error:", error);
    }
}
