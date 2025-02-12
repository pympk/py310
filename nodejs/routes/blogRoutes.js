const express = require('express');
// Import the Express.js library.

const blogController = require('../controllers/blogController');
// Import the blog controller functions.

const router = express.Router();
// Create an Express router instance.

router.get('/', blogController.blog_index);
// Route for displaying all blogs (GET request to '/').

router.post('/', blogController.blog_create_post);
// Route for creating a new blog (POST request to '/').

router.get('/create', blogController.blog_create_get);
// Route for displaying the new blog creation form (GET request to '/create').

router.get('/:id', blogController.blog_details);
// Route for displaying a single blog by ID (GET request to '/:id').

router.delete('/:id', blogController.blog_delete);
// Route for deleting a blog by ID (DELETE request to '/:id').

module.exports = router;
// Export the router to be used by the main application.
