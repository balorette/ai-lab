# Sales Agent System

A production-ready automated cold email generation and sending system using OpenAI agents.

## Features

- **Multi-Agent Architecture**: Three specialized sales agents (Professional, Engaging, Concise)
- **Email Management**: Automated subject line generation and HTML formatting
- **SendGrid Integration**: Production email delivery with proper error handling
- **Configuration Management**: Environment-based configuration
- **Logging**: Comprehensive logging for monitoring and debugging
- **Error Handling**: Robust error handling for production use

## Setup

1. Install dependencies:
```bash
pip install -r requirements-production.txt
```

2. Configure environment variables:
```bash
cp .env.template .env
# Edit .env with your configuration
```

3. Set up SendGrid:
   - Create a SendGrid account
   - Generate an API key
   - Verify your sender email address
   - Add the API key to your .env file

## Usage

### Basic Usage

```python
import asyncio
from openai_agents import SalesAgentSystem, EmailConfig

async def main():
    # Load configuration
    config = EmailConfig.from_env()
    
    # Initialize system
    sales_system = SalesAgentSystem(config)
    
    # Generate and send email
    result = await sales_system.generate_and_send_email(
        "Send a cold sales email to the CEO of TechCorp"
    )
    
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Configuration

```python
# Custom configuration
config = EmailConfig(
    from_email="sales@yourcompany.com",
    default_to_email="prospect@targetcompany.com",
    sendgrid_api_key="your_api_key"
)

# Use different model
sales_system = SalesAgentSystem(config, model="gpt-4")
```

## Environment Variables

- `SENDGRID_API_KEY`: Your SendGrid API key (required)
- `FROM_EMAIL`: Verified sender email address
- `DEFAULT_TO_EMAIL`: Default recipient email address
- `OPENAI_API_KEY`: Your OpenAI API key (if required by agents library)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Architecture

The system uses a hierarchical agent structure:

1. **Sales Manager**: Coordinates the email generation process
2. **Sales Agents**: Three specialized agents for different email styles
3. **Email Manager**: Handles formatting and delivery
4. **Support Agents**: Subject writer and HTML converter

## Production Considerations

- Ensure SendGrid API limits are appropriate for your use case
- Monitor email delivery rates and reputation
- Implement rate limiting for large-scale deployments
- Consider adding email template validation
- Set up monitoring and alerting for failed email deliveries

## Error Handling

The system includes comprehensive error handling:
- SendGrid API errors
- Network connectivity issues
- Configuration validation
- Agent processing errors

All errors are logged with appropriate detail for debugging.
