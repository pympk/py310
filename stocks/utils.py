import os
import time
import datetime

def get_latest_downloaded_files(directory_path, num_files=10):
    """
    Returns the N most recent files in a directory, sorted by modification time.

    Args:
        directory_path (str): The path to the directory to search.
        num_files (int): The number of files to list (default: 10).

    Returns:
        list: A list of tuples, where each tuple contains:
              (filename, file_size_bytes, last_modified_time)
              Returns an empty list if the directory doesn't exist or is empty.
    """

    # Check if the directory exists
    if not os.path.exists(directory_path):
        return []

    # Get a list of all files in the directory
    file_list = []
    try:
        # Iterate over all files in the directory
        for filename in os.listdir(directory_path):
            filepath = os.path.join(directory_path, filename)
            # Check if the file is a regular file (not a directory)
            if os.path.isfile(filepath):
                # Get the size of the file
                file_size = os.path.getsize(filepath)
                # Get the last modification time of the file
                last_modified_time = os.path.getmtime(filepath)
                # Add the file to the list
                file_list.append((filename, file_size, last_modified_time))

        # Sort the list of files by modification time
        file_list.sort(key=lambda x: x[2], reverse=True)

        # Return the top N files
        return file_list[:num_files]
    except OSError:
        # If there is an error, return an empty list
        return []


def main():
    """
    Main function to retrieve and display the largest files from the user's Downloads directory.

    This function fetches a specified number of the most recent files from the user's Downloads
    directory, sorts them by size in descending order, and prints their details including
    name, formatted size, and last modified time.

    The function is designed to be executed on Windows systems and uses the `get_latest_downloaded_files`
    utility to retrieve file information.
    """
    num_files = 5
    downloads_dir = os.path.expanduser("~\\Downloads")
    recent_files = get_latest_downloaded_files(downloads_dir, num_files)

    if recent_files:
        recent_files.sort(key=lambda x: x[1], reverse=True)
        print(f"{num_files} Largest Files in latest Downloads:")
        for filename, size, last_modified_time in recent_files:
            formatted_size = _format_size(size)
            formatted_time = datetime.datetime.fromtimestamp(last_modified_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"  - Name: {filename}")
            print(f"    Size: {formatted_size}")
            print(f"    Last Modified: {formatted_time}")
    else:
        print("No files found in the Downloads directory.")


def _format_size(size_bytes):
    """
    Formats a size in bytes to a readable string.
    """
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024
    if size_mb > 1:
        return f"{size_mb:.2f} MB"
    elif size_kb > 1:
        return f"{size_kb:.2f} KB"
    else:
        return f"{size_bytes} bytes"

if __name__ == "__main__":
    main()