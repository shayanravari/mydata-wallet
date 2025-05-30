document.getElementById('captureBtn').addEventListener('click', async () => {
    const rawData = document.getElementById('dataInput').value;
    if (rawData) {
        const parts = rawData.split(',');
        if (parts.length < 2) {
            document.getElementById('status').textContent = 'Format: Item,Price[,Category]';
            return;
        }
        const item_name = parts[0].trim();
        const amount = parseFloat(parts[1].trim());
        const category = parts.length > 2 ? parts[2].trim() : "Uncategorized";

        if (isNaN(amount)) {
            document.getElementById('status').textContent = 'Invalid price.';
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/ingest', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ item_name, amount, category }),
            });
            if (response.ok) {
                const result = await response.json();
                document.getElementById('status').textContent = `Data sent! ID: ${result.receipt_id}`;
                document.getElementById('dataInput').value = '';
            } else {
                document.getElementById('status').textContent = `Error: ${response.statusText}`;
            }
        } catch (error) {
            document.getElementById('status').textContent = `Network error: ${error.message}`;
            console.error("Error sending data:", error);
        }

    } else {
        document.getElementById('status').textContent = 'No data entered.';
    }
});