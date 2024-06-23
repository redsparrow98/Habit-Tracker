# Habit Tracker

This repository contains a simple Habit Tracker project created as a practice to understand HTTP POST, PUT, and DELETE 
requests using an API. The project is designed to help users track their habits by adding, updating, and deleting habit 
entries.

## Features

- **Create User** Use HTTP POST request to register user with Pixela.
- **Add Habits**: Use HTTP POST requests to add new habit data(pixel).
- **Update Habits**: Use HTTP PUT requests to update existing habit data(pixel).
- **Delete Habits**: Use HTTP DELETE requests to remove habit data(pixel).

## Future Plans

I plan to enhance this project by adding a user interface (UI) to make it more user-friendly and visually appealing.

## How to Use

1. Clone the repository:
    ```bash
    git clone https://github.com/redsparrow98/Habit-Tracker.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Habit-Tracker
    ```
3. Follow the steps in the code to understand how to make HTTP requests to the API.

## Environment Variables

This project uses a `.env` file to keep tokens and user information safe. If you wish to use the program, 
ensure you use the `dotenv` module to load these environment variables.

1. Install the `dotenv` module:
    ```bash
    pip install python-dotenv
    ```
2. Create a `.env` file in the project directory and add your tokens and user information for the Pixela API:
    ```env
    PIXELA_USER_TOKEN=your_api_token
    PIXELA_USERNAME=your_user_id
    ```
3. Find and Load the environment variables in your script:
    ```python
    from dotenv import find_dotenv, load_dotenv
    import os
    
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    PIXELA_USER_TOKEN = os.getenv('PIXELA_USER_TOKEN')
    PIXELA_USERNAME = os.getenv('PIXELA_USERNAME')
    ```

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss 
what you would like to change.

## Contact

If you have any questions or feedback, please reach out to me at prosicnatalija98@gmail.com.

---

*Note: This is a practice project aimed at learning and understanding basic API operations. It will be updated with more
features and a UI in the future.*

