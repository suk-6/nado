const hanspell = require('hanspell');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

const end = () => { };

const error = (err) => {
    console.error('error: ' + err);
};

app.post('/', async (req, res) => {
    const { text } = req.body;
    hanspell.spellCheckByPNU(text, 6000, (data) => {
        res.json(data);
    }, end, error);
});

app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});