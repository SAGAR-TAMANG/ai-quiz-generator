# AI Quiz Generator

A simple Django web application that generates customized quiz questions on any topic using AI.

## Features

- **Topic-based Quiz Generation**: Create quizzes on any subject instantly
- **Customizable Difficulty Levels**: Choose between easy, medium, and hard questions
- **Adjustable Quiz Length**: Generate between 5-20 questions per quiz
- **Interactive UI**: Show/hide answers with toggle buttons
- **Responsive Design**: Works on desktop and mobile devices

## Demo

<!-- Check out the live demo: [AI Quiz Generator Demo](https://your-demo-link-here.com) -->
The Demo will be there soon.

## Installation

### Prerequisites

- Python 3.8+
- Django 4.0+
- API key for the AI service

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/SAGAR-TAMANG/ai-quiz-generator.git
   cd ai-quiz-generator
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your API key:
   ```
   SUTRA_API_KEY=your_api_key_here
   ```

5. Apply migrations:
   ```
   python manage.py migrate
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Open your browser and navigate to `http://127.0.0.1:8000/`

## Usage

1. Enter a topic for your quiz (e.g., "Ancient Egypt", "Machine Learning", "Solar System")
2. Select a difficulty level
3. Choose the number of questions (5-20)
4. Click "Generate Quiz"
5. View the generated questions and click "Show Answer" to reveal the answers

## Project Structure

```
ai-quiz-generator/
├── quiz/                 # Main application
│   ├── templates/           # HTML templates
│   │   ├── index.html       # Quiz generation form
│   │   └── quiz_results.html # Generated quiz display
│   ├── views.py             # View controllers
│   └── urls.py              # URL configuration
├── quiz_generator/          # Project settings
│   ├── settings.py          # Django settings
│   └── urls.py              # Project URL configuration
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables (create this file)
└── README.md                # This file
```

## Customization

- To modify the appearance, edit the CSS in the HTML templates
- To change the question generation logic, update the `generate_questions_with_openai` function in `views.py`
- To add more quiz options, modify the form in `index.html`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- Styled with [Bootstrap](https://getbootstrap.com/)
- AI-powered by [TWO AI's SUTRA API](https://www.two.ai/sutra)