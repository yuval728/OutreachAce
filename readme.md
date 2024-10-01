# OutReachAce

This project is a Streamlit application designed to help users generate cold emails, skill gap analyses, and cover letters based on their resume and job postings.

## Features

- Upload your resume in PDF format.
- Input a job URL to fetch job details.
- Generate cold emails, skill gap analyses, and cover letters.
- Option to use only links from the resume.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Yuval728/cold-email-generator.git
    cd cold-email-generator
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file and add your API key:
    ```env
    API_KEY=your_api_key_here
    ```

## Usage

Run the Streamlit application:
```sh
streamlit run app/main.py
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.


