document.getElementById("send").addEventListener("click", async () => {
    const input = document.getElementById("userInput").value;
    const respEl = document.getElementById("response");
    respEl.innerText = "Loading...";
    try {
        const res = await fetch("http://localhost:8080/query", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ input })
        });
        if (!res.ok) throw new Error(`Server returned ${res.status}`);
        const data = await res.json();
        respEl.innerText = data.response ?? "[no response]";
    } catch (err) {
        respEl.innerText = "Error: " + err.message;
    }
});