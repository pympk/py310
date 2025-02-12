const trashcan = document.querySelector('a.delete');
// Select the delete link element.

trashcan.addEventListener('click', (e) => {
  // Add a click event listener to the delete link.
  const endpoint = `/blogs/${trashcan.dataset.doc}`;
  // Construct the API endpoint using the blog's ID from data attribute.

  // Ajax request to delete a blog entry
  fetch(endpoint, {
    // Send a DELETE request to the API endpoint.
    method: 'DELETE',
    // Specify the HTTP method as DELETE.
  })
    .then((response) => response.json())
    // Parse the JSON response.
    // .then((data) => console.log(data)) // commented out console.log statement.
    .then((data) => (window.location.href = data.redirect))
    // Redirect the user to the specified URL after deletion.
    .catch((err) => console.log(err));
  // Handle and log any errors during the fetch operation.
});
