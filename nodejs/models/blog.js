const mongoose = require('mongoose');
// Import the Mongoose library.

const Schema = mongoose.Schema;
// Get the Mongoose Schema constructor.

// Schema definition for blog data
const blogSchema = new Schema(
  // Create a new schema with defined fields.
  {
    title: {
      type: String,
      required: true,
      // Title field, String type, required.
    },
    snippet: {
      type: String,
      required: true,
      // Snippet field, String type, required.
    },
    body: {
      type: String,
      required: true,
      // Body field, String type, required.
    },
  },
  { timestamps: true }
  // Add timestamp fields (createdAt, updatedAt).
);

// Create a model based on the schema
const Blog = mongoose.model('blogs', blogSchema);
// Create the 'Blog' model, uses the 'blogs' collection.

module.exports = Blog;
// Export the Blog model for use in other modules.
