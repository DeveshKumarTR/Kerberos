# Contributing to Kerberos Protocol Implementation

We love your input! We want to make contributing to the Kerberos Protocol Implementation as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](https://github.com/DeveshKumarTR/Kerberos/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/DeveshKumarTR/Kerberos/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Setup

### Backend Development

```bash
# Clone the repository
git clone https://github.com/DeveshKumarTR/Kerberos.git
cd Kerberos/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run tests
python -m pytest tests/ -v

# Run the application
python app.py
```

### Frontend Development

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npx expo start

# Run tests
npm test

# Run linting
npm run lint
```

## Code Style Guidelines

### Python (Backend)

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://github.com/psf/black) for code formatting
- Use [flake8](https://flake8.pycqa.org/) for linting
- Document all functions and classes with docstrings
- Write type hints for function parameters and return values

```python
def authenticate_user(username: str, password: str) -> Dict[str, Any]:
    """
    Authenticate user credentials and return authentication result.
    
    Args:
        username: The username to authenticate
        password: The password to verify
        
    Returns:
        Dictionary containing authentication result and user data
    """
    # Implementation here
    pass
```

### TypeScript (Frontend)

- Use TypeScript for all new code
- Follow [TypeScript Style Guide](https://github.com/basarat/typescript-book/blob/master/docs/styleguide/styleguide.md)
- Use [ESLint](https://eslint.org/) and [Prettier](https://prettier.io/) for code formatting
- Use meaningful component and variable names
- Document complex components with JSDoc comments

```typescript
interface AuthResponse {
  success: boolean;
  token?: string;
  user?: User;
  error?: string;
}

/**
 * Authenticate user with provided credentials
 */
const authenticateUser = async (credentials: UserCredentials): Promise<AuthResponse> => {
  // Implementation here
};
```

## Testing Guidelines

### Backend Testing

- Write unit tests for all functions
- Use pytest for testing framework
- Test both success and failure cases
- Mock external dependencies (AI APIs, databases)
- Maintain test coverage above 90%

```python
def test_user_authentication_success():
    """Test successful user authentication."""
    # Arrange
    username = "testuser"
    password = "testpass"
    
    # Act
    result = authenticate_user(username, password)
    
    # Assert
    assert result["success"] is True
    assert "token" in result
```

### Frontend Testing

- Write unit tests for components and services
- Use Jest and React Native Testing Library
- Test user interactions and edge cases
- Mock API calls and external dependencies

```typescript
test('login screen renders correctly', () => {
  const { getByText, getByPlaceholderText } = render(<LoginScreen />);
  
  expect(getByText('Welcome')).toBeTruthy();
  expect(getByPlaceholderText('Username')).toBeTruthy();
  expect(getByPlaceholderText('Password')).toBeTruthy();
});
```

## Documentation Standards

- Update README.md for any new features
- Add JSDoc/docstring comments for all public functions
- Update API documentation for endpoint changes
- Include examples in documentation
- Keep documentation up to date with code changes

## Security Guidelines

- Never commit sensitive information (API keys, passwords, etc.)
- Use environment variables for configuration
- Validate all user inputs
- Follow OWASP security guidelines
- Review code for security vulnerabilities
- Update dependencies regularly

## Commit Message Guidelines

Use clear and meaningful commit messages:

```
feat: add user profile management
fix: resolve authentication token expiry issue
docs: update API documentation
test: add unit tests for encryption utilities
refactor: improve error handling in auth service
```

Format:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to contact the maintainer:
- **Devesh Kumar**: [GitHub Profile](https://github.com/DeveshKumarTR)
- **Email**: deveshkumar@example.com
- **Issues**: [GitHub Issues](https://github.com/DeveshKumarTR/Kerberos/issues)

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to make participation in our project and our community a harassment-free experience for everyone.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

---

**Thank you for contributing to the Kerberos Protocol Implementation!**

© 2025 Devesh Kumar. All rights reserved.
