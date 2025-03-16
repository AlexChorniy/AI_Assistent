require('dotenv').config();
const Imap = require('imap-simple');
const nodemailer = require('nodemailer');
const axios = require('axios'); // Assuming an AI API or local LLM like GPT4All

// IMAP Configuration
const imapConfig = {
  imap: {
    user: process.env.EMAIL_USER,
    password: process.env.EMAIL_PASS,
    host: process.env.IMAP_HOST,
    port: process.env.IMAP_PORT,
    tls: true,
    authTimeout: 3000
  }
};

// Connect to IMAP and fetch unread emails
async function fetchEmails() {
  try {
    const connection = await Imap.connect(imapConfig);
    await connection.openBox('INBOX');
    
    const searchCriteria = ['UNSEEN'];
    const fetchOptions = { bodies: ['HEADER', 'TEXT'], struct: true };
    const messages = await connection.search(searchCriteria, fetchOptions);

    for (let message of messages) {
      let text = message.parts.find(part => part.which === 'TEXT').body;
      console.log("\n📩 New Email:\n", text);

      // Summarize using AI (Example: local Llama.cpp API)
      let summary = await getAISummary(text);
      console.log("\n🤖 AI Summary:\n", summary);
    }

    connection.end();
  } catch (error) {
    console.error("Error fetching emails:", error);
  }
}

// AI Processing (Assuming a locally hosted AI model)
async function getAISummary(text) {
  try {
    const response = await axios.post('http://localhost:4000/api/summarize', { text });
    return response.data.summary;
  } catch (error) {
    return "AI failed to summarize.";
  }
}

// Run the script
fetchEmails();
