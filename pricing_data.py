# pricing_data.py
"""
All AI service pricing (updated October 2025)
Prices in USD per 1M tokens
"""

# API Services (per 1M tokens)
API_PRICING = {
    'openai': {
        'gpt-4.1': {'input': 2.10, 'output': 8.40, 'context': 1048000, 'tier': 'premium'},
        'gpt-4.1-mini': {'input': 0.42, 'output': 1.68, 'context': 1032000, 'tier': 'mid'},
        'gpt-4.1-nano': {'input': 0.105, 'output': 0.42, 'context': 1032000, 'tier': 'budget'},
        'gpt-4o': {'input': 2.50, 'output': 10.00, 'context': 128000, 'tier': 'premium'},
        'gpt-4o-mini': {'input': 0.15, 'output': 0.60, 'context': 128000, 'tier': 'budget'},
        'o4-mini': {'input': 1.16, 'output': 4.62, 'context': 200000, 'tier': 'mid'},
        'gpt-3.5-turbo': {'input': 0.50, 'output': 1.50, 'context': 16385, 'tier': 'budget'},
    },
    'anthropic': {
        'claude-opus-4.1': {'input': 15.00, 'output': 75.00, 'context': 200000, 'tier': 'premium'},
        'claude-sonnet-4.5': {'input': 3.00, 'output': 15.00, 'context': 1000000, 'tier': 'premium'},
        'claude-sonnet-4': {'input': 3.00, 'output': 15.00, 'context': 1000000, 'tier': 'premium'},
        'claude-haiku-4.5': {'input': 1.00, 'output': 5.00, 'context': 200000, 'tier': 'mid'},
        'claude-haiku-3.5': {'input': 0.80, 'output': 4.00, 'context': 200000, 'tier': 'mid'},
        'claude-haiku-3': {'input': 0.25, 'output': 1.25, 'context': 200000, 'tier': 'budget'},
    },
    'google': {
        'gemini-2.5-pro': {'input': 1.3125, 'output': 10.50, 'context': 1000000, 'tier': 'premium'},
        'gemini-2.5-flash': {'input': 0.30, 'output': 2.50, 'context': 1000000, 'tier': 'mid'},
        'gemini-2.5-flash-lite': {'input': 0.10, 'output': 0.40, 'context': 1000000, 'tier': 'budget'},
        'gemini-2.0-flash': {'input': 0.10, 'output': 0.40, 'context': 1000000, 'tier': 'budget'},
        'gemini-1.5-pro': {'input': 1.25, 'output': 5.00, 'context': 2000000, 'tier': 'mid'},
        'gemini-1.5-flash': {'input': 0.075, 'output': 0.30, 'context': 1000000, 'tier': 'budget'},
    },
    'deepseek': {
        'deepseek-v3.2-exp': {'input': 0.028, 'output': 0.11, 'context': 128000, 'tier': 'ultra-budget'},
        'deepseek-chat': {'input': 0.27, 'output': 1.10, 'context': 64000, 'tier': 'budget'},
        'deepseek-reasoner': {'input': 0.55, 'output': 2.19, 'context': 64000, 'tier': 'mid'},
    },
    'mistral': {
        'mistral-large': {'input': 2.00, 'output': 6.00, 'context': 128000, 'tier': 'premium'},
        'mistral-medium-3': {'input': 0.40, 'output': 1.20, 'context': 128000, 'tier': 'mid'},
        'mistral-small': {'input': 0.10, 'output': 0.30, 'context': 32000, 'tier': 'budget'},
    },
    'cohere': {
        'command-a': {'input': 2.77, 'output': 11.08, 'context': 256000, 'tier': 'premium'},
        'command-r-plus': {'input': 2.50, 'output': 10.00, 'context': 128000, 'tier': 'premium'},
        'command-r': {'input': 0.15, 'output': 0.60, 'context': 128000, 'tier': 'budget'},
    },
    'xai': {
        'grok-3-beta': {'input': 3.15, 'output': 15.75, 'context': 131000, 'tier': 'premium'},
        'grok-3-mini': {'input': 0.315, 'output': 0.525, 'context': 131000, 'tier': 'budget'},
    },
}

# Developer Tools (per user/month)
DEV_TOOLS = {
    'gitlab_duo': {'pro': 19, 'enterprise': 39},
    'github_copilot': {'individual': 10, 'business': 19, 'enterprise': 39},
    'cursor': {'pro': 20, 'business': 40},
    'codeium': {'individual': 0, 'teams': 12, 'enterprise': 35},
    'tabnine': {'pro': 12, 'enterprise': 39},
    'windsurf': {'pro': 10, 'team': 20}
}

# Team Subscriptions (per user/month)
TEAM_SUBS = {
    'chatgpt_plus': 20,
    'chatgpt_team': 25,
    'claude_pro': 20,
    'claude_team': 30,
}

# Use case routing rules
USE_CASE_ROUTING = {
    'customer_support': {'simple': 0.70, 'medium': 0.20, 'complex': 0.10},
    'content_generation': {'simple': 0.30, 'medium': 0.50, 'complex': 0.20},
    'code_generation': {'simple': 0.40, 'medium': 0.40, 'complex': 0.20},
    'document_analysis': {'simple': 0.50, 'medium': 0.30, 'complex': 0.20},
    'data_extraction': {'simple': 0.60, 'medium': 0.30, 'complex': 0.10}
}