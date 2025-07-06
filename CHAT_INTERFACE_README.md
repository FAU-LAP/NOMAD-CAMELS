# NOMAD-CAMELS AI Assistant Chat Interface

This feature adds a ChatGPT-like chat interface to NOMAD-CAMELS that helps users interact with the application using natural language.

## Features

- **Natural Language Interaction**: Ask questions about NOMAD-CAMELS in plain English
- **Sample Management**: AI can help you create new samples by asking for details
- **UI Integration**: Seamlessly integrated into the main window as a tab
- **Automatic Actions**: AI can perform actions like opening dialogs and creating samples
- **Secure**: Your OpenAI API key is stored locally and encrypted

## Setup

### 1. Install OpenAI Dependency

Make sure you have the OpenAI library installed:

```bash
pip install openai>=1.0.0
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Get OpenAI API Key

1. Go to [OpenAI's website](https://platform.openai.com/account/api-keys)
2. Create an account or log in
3. Generate a new API key
4. Copy the key (it starts with `sk-`)

### 3. Configure API Key in NOMAD-CAMELS

1. Start NOMAD-CAMELS
2. Look for the "AI Assistant" tab next to the "Console" tab
3. Click "Configure API Key"
4. Enter your OpenAI API key
5. Check "Save API key" to store it locally (recommended)

## Usage

### Basic Interaction

Simply type your questions or requests in the chat interface. Examples:

- "How do I add a new sample?"
- "What is NOMAD-CAMELS?"
- "Help me set up a measurement protocol"
- "I want to add a new sample"

### Sample Creation

The AI assistant can help you create new samples:

1. Type: "I want to add a new sample"
2. The AI will ask for sample details:
   - Sample name (required)
   - Sample ID (optional)
   - Description (optional)
3. Provide the information in natural language
4. The AI will create the sample and open the sample dialog

Example conversation:
```
You: I want to add a new sample
AI: I'd be happy to help you add a new sample! Please provide the following information:
    - Sample name (required)
    - Sample ID (optional)
    - Description (optional)

You: The sample name is "Silicon Wafer", ID is "SW-001", and it's a 4-inch silicon wafer for testing
AI: Perfect! I'll create the sample "Silicon Wafer" with ID "SW-001" now.
    ✅ Sample 'Silicon Wafer' has been successfully added!
    Sample ID: SW-001
    Description: 4-inch silicon wafer for testing
    Owner: your_username
```

### Available Commands

The AI assistant can help with:

- **Sample Management**: Create, understand, and manage samples
- **General Questions**: Learn about NOMAD-CAMELS features
- **Troubleshooting**: Get help with common issues
- **Workflow Guidance**: Step-by-step help with measurement procedures

## Technical Details

### Architecture

- **ChatInterface**: Main chat widget with message history
- **ChatWorker**: Background thread handling OpenAI API calls
- **Integration**: Seamlessly integrated into MainWindow as a tabbed interface
- **Security**: API keys stored in local preferences with encryption

### API Integration

- Uses OpenAI's GPT-3.5-turbo model
- Maintains conversation context (last 10 messages)
- Implements action-based responses for automated tasks
- Error handling for API failures and network issues

### Sample Integration

The chat interface directly integrates with NOMAD-CAMELS' sample management:

- Creates samples using the existing `sampledata` structure
- Updates the UI automatically when samples are created
- Opens sample dialogs to show created samples
- Maintains consistency with the existing sample management system

## Privacy and Security

- **Local Storage**: API keys are stored locally in your NOMAD-CAMELS preferences
- **No Data Sharing**: Your conversations and data are not stored by the chat interface
- **OpenAI Policy**: Conversations are subject to OpenAI's usage policies
- **Encryption**: Local storage uses standard preference encryption

## Troubleshooting

### Common Issues

1. **"OpenAI library not installed"**
   - Install with: `pip install openai>=1.0.0`

2. **"API Key Required"**
   - Configure your OpenAI API key in the settings

3. **"Error communicating with OpenAI"**
   - Check your internet connection
   - Verify your API key is valid
   - Ensure you have OpenAI credits available

4. **Chat interface not visible**
   - Check that the "AI Assistant" tab is present
   - Try restarting NOMAD-CAMELS
   - Ensure all dependencies are installed

### Getting Help

If you encounter issues:

1. Check the Console tab for error messages
2. Verify your OpenAI API key is valid
3. Ensure you have an active internet connection
4. Try restarting the application

## Future Enhancements

Potential future features:

- **Protocol Management**: AI assistance with creating and managing measurement protocols
- **Device Configuration**: Help with instrument setup and configuration
- **Data Analysis**: Basic data analysis and visualization assistance
- **Multi-language Support**: Support for languages other than English
- **Voice Interface**: Speech-to-text and text-to-speech capabilities

## Contributing

To contribute to the chat interface:

1. The main implementation is in `nomad_camels/gui/chat_interface.py`
2. Integration code is in `nomad_camels/MainApp_v2.py`
3. Follow the existing code style and patterns
4. Add appropriate error handling and logging
5. Test thoroughly with different scenarios

## License

This feature is part of NOMAD-CAMELS and follows the same license terms. 