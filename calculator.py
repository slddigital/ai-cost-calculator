# calculator.py
"""Core calculation logic"""
from pricing_data import API_PRICING, DEV_TOOLS, USE_CASE_ROUTING

def calculate_api_cost(provider, model, monthly_calls, avg_input_tokens, avg_output_tokens):
    """Calculate monthly cost for API usage"""
    pricing = API_PRICING[provider][model]
    input_cost = (monthly_calls * avg_input_tokens / 1_000_000) * pricing['input']
    output_cost = (monthly_calls * avg_output_tokens / 1_000_000) * pricing['output']
    return input_cost + output_cost

def find_cheapest_alternative(provider, model, monthly_calls, avg_input_tokens, avg_output_tokens):
    """Find cheapest model across all providers"""
    current_cost = calculate_api_cost(provider, model, monthly_calls, avg_input_tokens, avg_output_tokens)
    alternatives = []
    
    for alt_provider, models in API_PRICING.items():
        for alt_model, pricing in models.items():
            alt_cost = calculate_api_cost(alt_provider, alt_model, monthly_calls, avg_input_tokens, avg_output_tokens)
            if alt_cost < current_cost:
                savings_pct = ((current_cost - alt_cost) / current_cost) * 100
                alternatives.append({
                    'provider': alt_provider,
                    'model': alt_model,
                    'cost': alt_cost,
                    'savings': current_cost - alt_cost,
                    'savings_pct': savings_pct,
                })
    
    alternatives.sort(key=lambda x: x['savings'], reverse=True)
    return alternatives[:3]

def optimize_api_usage(provider, current_model, monthly_calls, avg_input_tokens, avg_output_tokens, use_case):
    """Suggest optimizations"""
    recommendations = []
    current_cost = calculate_api_cost(provider, current_model, monthly_calls, avg_input_tokens, avg_output_tokens)
    
    # Find cheaper alternatives
    alternatives = find_cheapest_alternative(provider, current_model, monthly_calls, avg_input_tokens, avg_output_tokens)
    
    if alternatives and alternatives[0]['savings'] > current_cost * 0.30:
        alt = alternatives[0]
        recommendations.append({
            'title': f'Switch to {alt["provider"].title()} {alt["model"]}',
            'description': f'Save {alt["savings_pct"]:.0f}% by switching providers',
            'current_cost': current_cost,
            'optimized_cost': alt['cost'],
            'monthly_savings': alt['savings'],
            'annual_savings': alt['savings'] * 12,
            'effort': 'Low',
            'implementation': f'1. Sign up for {alt["provider"].title()} API\n2. Update API endpoint\n3. Test with 10% of traffic\n4. Monitor quality\n5. Scale to 100%'
        })
    
    # Prompt caching recommendation
    if avg_input_tokens > 1000:
        caching_savings = current_cost * 0.30
        recommendations.append({
            'title': 'Enable prompt caching',
            'description': 'Cache repeated prompts to reduce costs 30-50%',
            'current_cost': current_cost,
            'optimized_cost': current_cost - caching_savings,
            'monthly_savings': caching_savings,
            'annual_savings': caching_savings * 12,
            'effort': 'Low',
            'implementation': 'Add caching parameters to API calls. Typical savings: 30-50%'
        })
    
    # Batch processing
    if monthly_calls > 100000:
        batch_savings = current_cost * 0.25
        recommendations.append({
            'title': 'Use Batch API (50% discount)',
            'description': 'Process non-urgent tasks overnight',
            'current_cost': current_cost,
            'optimized_cost': current_cost - batch_savings,
            'monthly_savings': batch_savings,
            'annual_savings': batch_savings * 12,
            'effort': 'Medium',
            'implementation': 'Identify non-urgent tasks and submit as batch jobs'
        })
    
    return recommendations

def analyze_dev_tools(tools_usage):
    """Analyze developer tool spending"""
    recommendations = []
    
    for tool, usage in tools_usage.items():
        if usage['total_seats'] == 0:
            continue
        
        tool_pricing = DEV_TOOLS.get(tool, {})
        if not tool_pricing:
            continue
        
        price_per_seat = tool_pricing.get('business', tool_pricing.get('pro', 0))
        current_cost = usage['total_seats'] * price_per_seat
        active_seats = usage.get('active_seats', usage['total_seats'])
        
        if active_seats < usage['total_seats']:
            wasted_seats = usage['total_seats'] - active_seats
            savings = wasted_seats * price_per_seat
            
            recommendations.append({
                'category': 'Developer Tools',
                'title': f'Remove {wasted_seats} unused {tool.replace("_", " ").title()} seats',
                'description': f'Only {active_seats} of {usage["total_seats"]} seats active',
                'current_cost': current_cost,
                'optimized_cost': active_seats * price_per_seat,
                'monthly_savings': savings,
                'annual_savings': savings * 12,
                'effort': 'Low',
                'implementation': f'Review usage logs and remove inactive users'
            })
    
    return recommendations

def generate_summary_report(all_recommendations):
    """Generate summary of all recommendations"""
    if not all_recommendations:
        return {
            'total_monthly_cost': 0,
            'total_annual_cost': 0,
            'total_monthly_savings': 0,
            'total_annual_savings': 0,
            'savings_percentage': 0,
            'top_recommendations': [],
            'all_recommendations': []
        }
    
    total_current_cost = sum(r.get('current_cost', 0) for r in all_recommendations)
    total_monthly_savings = sum(r.get('monthly_savings', 0) for r in all_recommendations)
    
    return {
        'total_monthly_cost': total_current_cost,
        'total_annual_cost': total_current_cost * 12,
        'total_monthly_savings': total_monthly_savings,
        'total_annual_savings': total_monthly_savings * 12,
        'savings_percentage': (total_monthly_savings / total_current_cost * 100) if total_current_cost > 0 else 0,
        'top_recommendations': sorted(all_recommendations, key=lambda x: x.get('annual_savings', 0), reverse=True)[:5],
        'all_recommendations': all_recommendations
    }