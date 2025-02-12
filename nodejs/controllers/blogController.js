const Blog = require('../models/blog');
// Import the Blog model.

const BLOG_INDEX_TITLE = 'All Blogs';
// Constant for the title of the blog index page.
const BLOG_DETAILS_TITLE = 'Blog details';
// Constant for the title of the blog details page.
const BLOG_CREATE_TITLE = 'Create a new blog';
// Constant for the title of the create blog page.
const HOME_REDIRECT = '/';
// Constant for the home page redirect URL.

const blog_index = async (req, res) => {
  // Controller for displaying all blogs.
  try {
    // Use try...catch to handle any errors during the process.
    const blogs = await Blog.find().sort({ createdAt: -1 });
    // Fetch all blogs, sorted by creation date.
    res.render('blogs/index', { title: BLOG_INDEX_TITLE, blogs });
    // Render the 'index' view with blog data and the specified title constant.
  } catch (err) {
    console.error('Error in blog_index:', err);
    // Log a more detailed error message, including the function name.
    res.status(500).send('Internal Server Error');
    // Send a 500 Internal Server Error response for failed requests.
  }
};

const blog_details = async (req, res) => {
  // Controller for displaying a single blog.
  const id = req.params.id;
  // Extract blog ID from request parameters.
  try {
    // Use try...catch to handle any errors during the process.
    const blog = await Blog.findById(id);
    // Find a blog by its ID.
    if (!blog) {
      // Check if blog is found or not
      return res.status(404).render('404', { title: 'Blog not found' });
      // Render 404 page if blog is not found.
    }
    console.log(`result = ${blog}`);
    // Log the result.
    res.render('blogs/details', { blog, title: BLOG_DETAILS_TITLE });
    // Render the 'details' view with blog data and the specified title constant.
  } catch (err) {
    console.error('Error in blog_details:', err);
    // Log a more detailed error message, including the function name.
    res.status(500).send('Internal Server Error');
    // Send a 500 Internal Server Error response for failed requests.
  }
};

const blog_create_get = (req, res) => {
  // Controller for displaying the create blog form.
  res.render('blogs/create', { title: BLOG_CREATE_TITLE });
  // Render the 'create' view with the specified title constant.
};

const blog_create_post = async (req, res) => {
  // Controller for creating a new blog post.
  console.log(req.body);
  // Log the request body.
  const blog = new Blog(req.body);
  // Create a new blog instance from request body.
  try {
    // Use try...catch to handle any errors during the process.
    await blog.save();
    // Save the blog instance to the database.
    res.redirect(HOME_REDIRECT);
    // Redirect the user to the home page after successful creation.
  } catch (err) {
    console.error('Error in blog_create_post:', err);
    // Log a more detailed error message, including the function name.
    res.status(500).send('Internal Server Error');
    // Send a 500 Internal Server Error response for failed requests.
  }
};

const blog_delete = async (req, res) => {
  // Controller for deleting a blog.
  const id = req.params.id;
  // Extract blog ID from request parameters.
  try {
    // Use try...catch to handle any errors during the process.
    await Blog.findByIdAndDelete(id);
    // Find and delete the blog by ID.
    res.json({ redirect: HOME_REDIRECT });
    // Send a JSON response with redirect URL.
  } catch (err) {
    console.error('Error in blog_delete:', err);
    // Log a more detailed error message, including the function name.
    res.status(500).send('Internal Server Error');
    // Send a 500 Internal Server Error response for failed requests.
  }
};

module.exports = {
  // Export all controller functions for routing.
  blog_index,
  blog_details,
  blog_create_get,
  blog_create_post,
  blog_delete,
};
