const Blog = require('../models/blog');

const blog_index = (req, res) => {
  Blog.find()
    .sort({ createdAt: -1 })
    .then((result) => {
      res.render('blogs/index', { title: 'All Blogs', blogs: result });
    })
    .catch((err) => {
      console.log(err);
    });
};

const blog_details = (req, res) => {
  const id = req.params.id;
  Blog.findById(id)
    .then((result) => {
      console.log(`result = ${result}`);
      res.render('blogs/details', { blog: result, title: 'Blog details' });
    })
    .catch((err) => {
      console.log(err);

      res.status(404).render('404', { title: 'Blog not found' });
    });
};

const blog_create_get = (req, res) => {
  res.render('blogs/create', { title: 'Create a new blog' });
};

const blog_create_post = (req, res) => {
  console.log(req.body);
  const blog = new Blog(req.body);
  blog
    // This returns a promise
    .save()
    .then((result) => {
      // Handle success
      res.redirect('/');
    })
    .catch((err) => {
      // Handel errors
      console.log(err);
    });
};

const blog_delete = (req, res) => {
  const id = req.params.id;
  Blog.findByIdAndDelete(id)
    .then((result) => {
      res.json({ redirect: '/' });
    })
    .catch((err) => {
      console.log(err);
    });
};

module.exports = {
  blog_index,
  blog_details,
  blog_create_get,
  blog_create_post,
  blog_delete,
};
