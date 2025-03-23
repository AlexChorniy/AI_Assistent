const express = require('express');
const app = express();
app.use(express.json());

// Handle GET request at root
app.get('/', (req, res) => {
  res.send('Llama server is running!');
});

// Handle POST request for summarization
app.post('/api/summarize', (req, res) => {
    const text = req.body.text;
    const summary = text.slice(0, 100) + "..."; // Mock summarization
    res.json({ summary });
});

const PORT = 5050;
app.listen(PORT, () => console.log(`Llama server running on port ${PORT}`));
