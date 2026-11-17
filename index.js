const express = require('express');
const dotenv = require('dotenv');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;
const API_URL = (process.env.API_URL || '').replace(/\/+$/, '');
const RAW_LOG_PATH = process.env.EFS_LOG_PATH || '';

/**
 * Resolve EFS log file path safely.
 * If EFS_LOG_PATH points to a directory (e.g., /home/ec2-user/efs), append app.log.
 */
function resolveLogFilePath(rawPath) {
    if (!rawPath) return null;
    try {
        if (fs.existsSync(rawPath) && fs.statSync(rawPath).isDirectory()) {
            return path.join(rawPath, 'app.log');
        }
    } catch (_) {
        // Fall through and treat as file path if stat fails
    }
    return path.extname(rawPath) ? rawPath : path.join(rawPath, 'app.log');
}

const LOG_FILE_PATH = resolveLogFilePath(RAW_LOG_PATH);

function writeAccessLog(req) {
    if (!LOG_FILE_PATH) return;
    const logLine = `${new Date().toISOString()} - ${req.method} ${req.originalUrl} - ${req.ip}\n`;
    fs.appendFile(LOG_FILE_PATH, logLine, (err) => {
        if (err) {
            console.error('Error writing to EFS log file:', err.message);
        }
    });
}

function requireApiUrl(res) {
    if (!API_URL) {
        res.status(500).json({ error: 'API_URL is not configured in .env' });
        return false;
    }
    return true;
}

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.use((req, res, next) => {
    writeAccessLog(req);
    next();
});

app.get('/health', (req, res) => {
    res.status(200).json({
        status: 'healthy',
        apiConfigured: Boolean(API_URL),
        efsLogPath: LOG_FILE_PATH || 'disabled'
    });
});

app.get('/api/books', async (req, res) => {
    if (!requireApiUrl(res)) return;
    try {
        const response = await axios.get(API_URL);
        res.status(200).json(response.data);
    } catch (error) {
        console.error('Error fetching books:', error.message);
        res.status(error.response?.status || 502).json({ error: 'Failed to fetch books from API Gateway' });
    }
});

app.get('/api/books/:id', async (req, res) => {
    if (!requireApiUrl(res)) return;
    try {
        const response = await axios.get(`${API_URL}/${encodeURIComponent(req.params.id)}`);
        res.status(200).json(response.data);
    } catch (error) {
        console.error('Error fetching book:', error.message);
        res.status(error.response?.status || 502).json({ error: 'Failed to fetch book from API Gateway' });
    }
});

app.post('/api/books', async (req, res) => {
    if (!requireApiUrl(res)) return;
    try {
        const response = await axios.post(API_URL, { title: req.body.title });
        res.status(response.status || 201).json(response.data);
    } catch (error) {
        console.error('Error creating book:', error.message);
        res.status(error.response?.status || 502).json({ error: 'Failed to create book via API Gateway' });
    }
});

app.put('/api/books/:id', async (req, res) => {
    if (!requireApiUrl(res)) return;
    try {
        const response = await axios.put(`${API_URL}/${encodeURIComponent(req.params.id)}`, {
            title: req.body.title
        });
        res.status(response.status || 200).json(response.data);
    } catch (error) {
        console.error('Error updating book:', error.message);
        res.status(error.response?.status || 502).json({ error: 'Failed to update book via API Gateway' });
    }
});

app.delete('/api/books/:id', async (req, res) => {
    if (!requireApiUrl(res)) return;
    try {
        const response = await axios.delete(`${API_URL}/${encodeURIComponent(req.params.id)}`);
        res.status(response.status || 200).json(response.data);
    } catch (error) {
        console.error('Error deleting book:', error.message);
        res.status(error.response?.status || 502).json({ error: 'Failed to delete book via API Gateway' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
