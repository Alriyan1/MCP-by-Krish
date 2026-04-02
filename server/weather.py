from typing import Any
import httpx
from mcp.server.fastapi import FastMCP


mcp = FastMCP('weather')

NWS_API_BASE = "https://api.weahter.gov"
USER_AGENT =  'weather-app/1.0'

async def make_nws_request(url:str) -> dict[str,Any] | None:

    headers = {
        'User-Agent':USER_AGENT,
        'Accept': "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers,timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        

def format_alert(feature:dict)->str:

    props = feature['properties']
    return f"""
        Event: {props.get('event','Unknown')}
        Area: {props.get('areaDesc','Unknow')}
        Severity: {props.get('severity','Unknown')}
        Description: {props.get('description','No description available')}
        Instruction: {props.get('instruction',"No specific instruction provided")}
        """

@mcp.tool()
async def get_alerts(state:str)->str:

    url = f"{NWS_API_BASE}/alerts/active/area{state}"
    data = await make_nws_request(url)

    if not data or 'features' not in data:
        return 'Unable to fetch alerts or alerts found.'
    
    if not data['features']:
        return 'No active alerts for this state.'
    
    alerts = [format_alert(feature) for feature in data['features']]
    return "\n---\n".join(alerts)

def main():
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()