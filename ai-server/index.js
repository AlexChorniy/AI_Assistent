// Disable SSL certificate validation (temporary fix for self-signed certs)
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

const axios = require('axios');
const Imap = require('imap-simple');

const imapConfig = {
  imap: {
    user: process.env.EMAIL_USER,
    password: process.env.EMAIL_PASS,
    host: process.env.IMAP_HOST,
    port: process.env.IMAP_PORT,
    tls: true,
  }
};

async function fetchEmails() {
  try {
    const connection = await Imap.connect(imapConfig);
    await connection.openBox('INBOX');

    const messages = await connection.search(['UNSEEN'], { bodies: ['TEXT'] });

    for (let msg of messages) {
      let text = msg.parts.find(part => part.which === 'TEXT').body;
      console.log("📩 Email:", text);

      let summary = await summarizeText(text);
      console.log("🤖 AI Summary:", summary);
    }

    connection.end();
  } catch (error) {
    console.error("Error fetching emails:", error);
  }
}

async function summarizeText(text) {
  try {
    const response = await axios.post(process.env.AI_API_URL, { text });
    return response.data.summary;
  } catch (error) {
    return "Failed to summarize.";
  }
}

fetchEmails();
