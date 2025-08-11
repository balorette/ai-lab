"""
Production-ready Sales Agent System for ComplAI
Automated cold email generation and sending system using OpenAI agents.
"""

import os
import asyncio
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
import re

from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv(override=True)


@dataclass
class EmailConfig:
    """Email configuration settings"""
    from_email: str
    default_to_email: str
    sendgrid_api_key: str
    
    @classmethod
    def from_env(cls) -> 'EmailConfig':
        """Create config from environment variables"""
        config = cls(
            from_email=os.getenv('FROM_EMAIL', 'bryan.a.lorette@gmail.com'),
            default_to_email=os.getenv('DEFAULT_TO_EMAIL', 'bryan.a.lorette@gmail.com'),
            sendgrid_api_key=os.getenv('SENDGRID_API_KEY', '')
        )
        config._validate()
        return config
    
    def _validate(self):
        """Validate email configuration"""
        if not self._is_valid_email(self.from_email):
            raise ValueError(f"Invalid from_email: {self.from_email}")
        if not self._is_valid_email(self.default_to_email):
            raise ValueError(f"Invalid default_to_email: {self.default_to_email}")
        if not self.sendgrid_api_key:
            logger.warning("SendGrid API key not configured - email sending will fail")
    
    def _is_valid_email(self, email: str) -> bool:
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))


class SalesAgentSystem:
    """Production-ready sales agent system for automated cold email generation"""
    
    def __init__(self, email_config: EmailConfig, model: str = "gpt-4o-mini"):
        self.email_config = email_config
        self.model = model
        self._setup_agents()
        self._setup_tools()
        
    def _setup_agents(self):
        """Initialize all sales agents"""
        # Sales Agent Instructions
        professional_instructions = """You are a professional sales agent working for ComplAI, 
        a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. 
        You write professional, serious cold emails that focus on business value and compliance benefits."""

        engaging_instructions = """You are a charismatic, engaging sales agent working for ComplAI, 
        a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. 
        You write witty, engaging cold emails that are likely to get a response while maintaining professionalism."""

        concise_instructions = """You are an efficient sales agent working for ComplAI, 
        a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. 
        You write concise, to-the-point cold emails that respect the recipient's time."""

        # Initialize Sales Agents
        self.professional_agent = Agent(
            name="Professional Sales Agent",
            instructions=professional_instructions,
            model=self.model
        )

        self.engaging_agent = Agent(
            name="Engaging Sales Agent", 
            instructions=engaging_instructions,
            model=self.model
        )

        self.concise_agent = Agent(
            name="Concise Sales Agent",
            instructions=concise_instructions,
            model=self.model
        )

        # Email formatting agents
        subject_instructions = """You write compelling subject lines for cold sales emails. 
        You are given an email body and create a subject that is likely to get opened while being honest and professional."""

        html_instructions = """You convert plain text email bodies to well-formatted HTML emails. 
        You create simple, clean, and compelling layouts that are mobile-friendly and professional."""

        self.subject_writer = Agent(
            name="Subject Writer",
            instructions=subject_instructions,
            model=self.model
        )

        self.html_converter = Agent(
            name="HTML Converter", 
            instructions=html_instructions,
            model=self.model
        )

    def _setup_tools(self):
        """Setup tools and email functions"""
        # Create agent tools
        description = "Write a cold sales email"
        self.professional_tool = self.professional_agent.as_tool(
            tool_name="professional_sales_agent", 
            tool_description=description
        )
        self.engaging_tool = self.engaging_agent.as_tool(
            tool_name="engaging_sales_agent", 
            tool_description=description
        )
        self.concise_tool = self.concise_agent.as_tool(
            tool_name="concise_sales_agent", 
            tool_description=description
        )
        
        # Create email formatting tools
        self.subject_tool = self.subject_writer.as_tool(
            tool_name="subject_writer", 
            tool_description="Write a subject for a cold sales email"
        )
        self.html_tool = self.html_converter.as_tool(
            tool_name="html_converter",
            tool_description="Convert a text email body to an HTML email body"
        )
        
        # Setup manager agents
        self._setup_managers()
    
    def _setup_managers(self):
        """Setup sales manager and email manager agents"""
        # Email Manager Agent
        email_manager_instructions = """You are an email formatter and sender. You receive the body of an email to be sent. 
        You first use the subject_writer tool to write a subject for the email, then use the html_converter tool to convert the body to HTML. 
        Finally, you use the send_html_email tool to send the email with the subject and HTML body."""

        self.email_manager = Agent(
            name="Email Manager",
            instructions=email_manager_instructions,
            tools=[self.subject_tool, self.html_tool, self._create_send_html_email_tool()],
            model=self.model,
            handoff_description="Convert an email to HTML and send it"
        )

        # Sales Manager Agent
        sales_manager_instructions = """You are a sales manager working for ComplAI. You use the tools given to you to generate cold sales emails. 
        You never generate sales emails yourself; you always use the tools. 
        You try all 3 sales agent tools at least once before choosing the best one. 
        You can use the tools multiple times if you're not satisfied with the results from the first try. 
        You select the single best email using your own judgment of which email will be most effective. 
        After picking the email, you handoff to the Email Manager agent to format and send the email."""

        self.sales_manager = Agent(
            name="Sales Manager",
            instructions=sales_manager_instructions,
            tools=[self.professional_tool, self.engaging_tool, self.concise_tool],
            handoffs=[self.email_manager],
            model=self.model
        )
    
    def _create_send_html_email_tool(self):
        """Create the send HTML email tool with proper error handling"""
        @function_tool
        def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
            """Send out an email with the given subject and HTML body to all sales prospects"""
            try:
                if not self.email_config.sendgrid_api_key:
                    logger.error("SendGrid API key not configured")
                    return {"status": "error", "message": "Email service not configured"}
                
                sg = sendgrid.SendGridAPIClient(api_key=self.email_config.sendgrid_api_key)
                from_email = Email(self.email_config.from_email)
                to_email = To(self.email_config.default_to_email)
                content = Content("text/html", html_body)
                mail = Mail(from_email, to_email, subject, content).get()
                
                response = sg.client.mail.send.post(request_body=mail)
                
                if response.status_code == 202:
                    logger.info(f"Email sent successfully: {subject}")
                    return {"status": "success", "message": f"Email sent with subject: {subject}"}
                else:
                    logger.error(f"Failed to send email: {response.status_code}")
                    return {"status": "error", "message": f"Failed to send email: {response.status_code}"}
                    
            except Exception as e:
                logger.error(f"Error sending email: {str(e)}")
                return {"status": "error", "message": f"Error sending email: {str(e)}"}
        
        return send_html_email
    
    async def generate_and_send_email(self, message: str) -> Dict[str, str]:
        """Generate and send a cold sales email based on the message"""
        try:
            logger.info(f"Starting email generation with message: {message}")
            
            with trace("Automated SDR"):
                result = await Runner.run(self.sales_manager, message)
                
            logger.info("Email generation completed successfully")
            return {"status": "success", "result": result.final_output}
            
        except Exception as e:
            logger.error(f"Error in email generation: {str(e)}")
            return {"status": "error", "message": str(e)}


async def main():
    """Main function to demonstrate the sales agent system"""
    try:
        # Load configuration from environment
        email_config = EmailConfig.from_env()
        
        # Validate configuration
        if not email_config.sendgrid_api_key:
            logger.error("SENDGRID_API_KEY environment variable is required")
            return
        
        # Initialize sales agent system
        sales_system = SalesAgentSystem(email_config)
        
        # Generate and send email
        message = "Send out a cold sales email addressed to Dear CEO from Alice"
        result = await sales_system.generate_and_send_email(message)
        
        if result["status"] == "success":
            logger.info("Sales email process completed successfully")
        else:
            logger.error(f"Sales email process failed: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        logger.error(f"Main execution error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())