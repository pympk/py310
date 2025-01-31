const express = require('express');
const morgan = require('morgan');
const mongoose = require('mongoose');
const blogRoutes = require('./routes/blogRoutes1');

require('dotenv').config({ path: '../../.env/my_api_key.env' }); // Fixed path
const dbURI = process.env.DB_URI;

// express app
const app = express();

// Connect to mongodb
mongoose
  .connect(dbURI)
  .then((result) => {
    console.log('Connected to db');
    app.listen(3000, () => {
      console.log('Sever listening on port 3000');
    });
  })
  .catch((err) => console.log(err));

// register view engine
app.set('view engine', 'ejs');

// middleware & static files
app.use(express.static('public'));

// Create object for Post
app.use(express.urlencoded({ extended: true }));
app.use(morgan('dev'));

// routes
app.get('/', (req, res) => {
  res.redirect('/blogs');
});

app.get('/about', (req, res) => {
  res.render('about', { title: 'About' });
});

// blog routes
app.use('/blogs', blogRoutes);

// 404 page
app.use((req, res) => {
  res.status(404).render('404', { title: '404' });
});
