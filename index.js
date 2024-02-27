const express = require('express');
const dotenv = require('dotenv');
const axios = require('axios');

const app = express();
dotenv.config();

const API_URL = process.env.API_URL;

app.use(express.static('public'));
app.use(express.json());

app.set('view engine', 'ejs');

app.get('/', (req, res) => {
    const ip_address = req.ip;
    res.render('index', { ip_address });
});

app.get('/get_books', async (req, res) => {
    try {
        const response = await axios.get(API_URL);
        const books = response.data;
        res.json(books);
    } catch (error) {
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.post('/add_book', (req, res) => {
    const { title } = req.body;
    // Logic to add book
    res.json({ message: 'Book added successfully' });
});

app.listen(5000, () => {
    console.log('Server is running on port 5000');
});
