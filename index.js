const express = require('express');
const app = express();
var expressLayouts = require('express-ejs-layouts');

app.set('view engine', 'ejs');
app.use(expressLayouts);

app.get('/', (req, res) => {
    res.render('index.ejs');
});

app.listen(3000, () => {
    console.log('Server started on port 3000');
});