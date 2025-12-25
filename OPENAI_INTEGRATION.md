# OpenAI Integration Guide

This document explains how to integrate and use OpenAI API with your Physical AI Book project.

## Overview

The project now supports multiple LLM providers including OpenAI, Groq, and Google Gemini. The system is designed to be flexible and configurable while maintaining backward compatibility.

## Configuration

### Environment Variables

To use OpenAI, configure the following environment variables in your `.env` file:

```env
# LLM Configuration
LLM_API_KEY=your_openai_api_key_here
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-3.5-turbo
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=1000
```

### Supported Providers

| Provider | LLM_PROVIDER Value | Notes |
|----------|-------------------|-------|
| OpenAI | `openai` | Default provider |
| Groq | `groq` | Fast inference for open models |
| Google Gemini | `gemini` | Google's LLM service |

### Model Options

- **OpenAI**: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`, etc.
- **Groq**: `llama3-70b-8192`, `llama2-70b-4096`, etc.
- **Gemini**: `gemini-pro`, `gemini-1.5-pro`, etc.

## Implementation Details

### Backend Changes

The following files were updated to support OpenAI integration:

1. **`backend/routers/chat.py`**:
   - Enhanced `call_llm_api` function to support multiple providers
   - Added provider-specific API endpoint routing
   - Implemented proper error handling for each provider

2. **`backend/config.py`**:
   - Added new configuration options for LLM providers
   - Added provider-specific model configuration

3. **`.env.example` and `backend/.env.example`**:
   - Updated with new configuration options
   - Added OpenAI-specific defaults

### API Call Flow

1. The system reads the `LLM_PROVIDER` environment variable
2. Based on the provider, it selects the appropriate API endpoint
3. The request is formatted according to the provider's API specification
4. Response is processed and returned to the frontend

## Usage Examples

### Using OpenAI (Default)

```env
LLM_API_KEY=sk-your-openai-api-key-here
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-3.5-turbo
```

### Using Groq

```env
LLM_API_KEY=your-groq-api-key-here
LLM_PROVIDER=groq
GROQ_MODEL=llama3-70b-8192
```

### Using Google Gemini

```env
LLM_API_KEY=your-gemini-api-key-here
LLM_PROVIDER=gemini
GEMINI_MODEL=gemini-pro
```

## Testing

To verify your OpenAI integration is working:

1. Set your OpenAI API key in the environment variables
2. Ensure `LLM_PROVIDER=openai`
3. Start the backend server
4. Make a request to the `/api/v1/chat` endpoint

## Troubleshooting

### Common Issues

1. **API Key Not Working**:
   - Verify your API key is correct
   - Check that billing is enabled for your account (for OpenAI)
   - Ensure the environment variable is properly set

2. **Provider Not Recognized**:
   - Make sure `LLM_PROVIDER` is set to a valid value
   - Default is `openai` if not specified

3. **Rate Limiting**:
   - Check your provider's rate limits
   - The application includes built-in rate limiting
   - Monitor usage through the `/api/v1/monitoring/usage` endpoint

## Security Considerations

- Never commit API keys to version control
- Use environment variables for sensitive information
- Rotate API keys regularly
- Monitor API usage to prevent abuse