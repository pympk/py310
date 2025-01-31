const mongoose = require("mongoose"); // create object
const Schema = mongoose.Schema; // Schema is the data structure

// Create instance of Schema object
// Schema defines the data structure
const blogSchema = new Schema(
  {
    title: {
      type: String,
      required: true,
    },
    snippet: {
      type: String,
      required: true,
    },
    body: {
      type: String,
      required: true,
    },
  },
  { timestamps: true }
);

// mongoose.model('Blog') will search
//  database collection for the plural of blog
const Blog = mongoose.model("Blog", blogSchema);
module.exports = Blog;

// const mongoose = require("mongoose");
// const Schema = mongoose.Schema;

// const blogSchema = new Schema(
//   {
//     title: {
//       type: String,
//       required: true,
//     },
//     snippet: {
//       type: String,
//       required: true,
//     },
//     body: {
//       type: String,
//       required: true,
//     },
//   },
//   { timestamps: true }
// );

// const Blog = mongoose.model("Blog", blogSchema);
// module.exports = Blog;
