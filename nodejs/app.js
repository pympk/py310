// Import necessary modules (like libraries)
const express = require('express'); // Imports the Express.js framework for building web applications
const morgan = require('morgan'); // Imports Morgan for logging HTTP requests
const mongoose = require('mongoose'); // Imports Mongoose for interacting with MongoDB
const helmet = require('helmet'); // Imports Helmet for setting secure HTTP headers
const blogRoutes = require('./routes/blogRoutes'); // Imports custom routes for handling blog-related requests

// Load environment variables from a .env file
require('dotenv').config({ path: '../.env/my_api_key.env' }); // Reads environment variables defined in a .env file and makes them available in process.env

// Get the MongoDB connection URI (URL) from the environment variables
const dbURI = process.env.DB_URI; // Accesses the database URL from environment variables

// Create an Express application instance
const app = express();

// Set the port for the server. If the PORT environment variable is set, use that.
// Otherwise default to 3000
const port = process.env.PORT || 3000;

// Log a message to the console to indicate that the server is starting.
// This provides a helpful message in the console
console.log('Server is about to start...');

// Connect to MongoDB
mongoose
  .connect(dbURI) // Connects to the MongoDB database using the connection string from the environment variable
  .then(() => {
    // This part runs after a successful database connection
    console.log('Connected to MongoDB'); // Log a message to the console when the connection is successful
    // Start the server and listen for incoming HTTP requests on the specified port
    app.listen(port, () => {
      console.log(`Server listening on port ${port}`); // Log a message when the server is listening on the port
    });
  })
  .catch((err) => {
    // This part runs if there's an error during the database connection
    console.error('MongoDB connection error:', err); // Logs an error message if connection fails, including the error details
    process.exit(1); // Gracefully exits the Node.js process with an error code
  });

// Set the view engine for the Express application to EJS (Embedded JavaScript Templates)
app.set('view engine', 'ejs'); // Configures Express to use EJS for rendering HTML templates

// Middleware setup
app.use(express.static('public')); // Serves static files (like CSS, images) from the 'public' directory
app.use(express.urlencoded({ extended: true })); // Parses URL-encoded request bodies (e.g., data from forms)
app.use(morgan('dev')); // Logs HTTP requests in development format to the console
app.use(helmet()); // Sets up secure HTTP headers to protect from common web vulnerabilities

// Define routes for handling different HTTP requests
app.get('/', (req, res) => {
  // When a GET request is made to the root path ('/')
  res.redirect('/blogs'); // Redirects to the /blogs path
});

app.get('/about', (req, res) => {
  // When a GET request is made to the /about path
  res.render('about', { title: 'About' }); // Renders the 'about' view (an EJS file), passing 'About' as the title variable
});

// Use the blog routes for paths that start with `/blogs`
app.use('/blogs', blogRoutes); // Delegates requests starting with '/blogs' to the blogRoutes

// 404 error handler:
// This code will execute if no other routes matched the incoming request
app.use((req, res) => {
  // Catch-all for routes not explicitly defined
  res.status(404).render('404', { title: '404' }); // Renders the '404' view for requests that don't match any route, with '404' as the title
});

// Global error handler
// This middleware will catch errors that occur during the request lifecycle
app.use((err, req, res, next) => {
  // Custom error handler for the entire application
  console.error(err.stack); // Logs the error stack trace to the console
  res.status(500).render('500', { title: 'Server Error' }); // Renders the '500' view, indicating a server error
});
