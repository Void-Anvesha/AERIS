from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional

from app.services.geospatial import GeospatialAgent, GeospatialInput
from app.services.hotspot import HotspotAgent, HotspotInput
from app.core.exceptions import ValidationError, AERISException

router = APIRouter(tags=["agents"])

geospatial_agent = GeospatialAgent()
hotspot_agent = HotspotAgent()


@router.post("/geospatial/analyze")
def analyze_geospatial(input_data: GeospatialInput) -> Dict[str, Any]:
    """Execute Geospatial Intelligence Agent analysis for a location."""
    try:
        return geospatial_agent.analyze_location(input_data)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except AERISException as ae:
        raise HTTPException(status_code=400, detail=str(ae))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal agent error: {str(e)}")


@router.post("/hotspot/analyze")
def analyze_hotspot(input_data: HotspotInput) -> Dict[str, Any]:
    """Execute Hotspot & Event Detection Agent analysis for a location."""
    try:
        return hotspot_agent.analyze_hotspot(input_data)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except AERISException as ae:
        raise HTTPException(status_code=400, detail=str(ae))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal agent error: {str(e)}")
