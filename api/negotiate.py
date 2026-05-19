from fastapi import APIRouter
from pydantic import BaseModel
from core.embeddings import embed
from core.database import search_job_descriptions, search_candidate_profiles
from core.claude import get_negotiation_coaching, get_free_negotiation_coaching

router = APIRouter(prefix="/negotiate", tags=["negotiate"])


class OfferInput(BaseModel):
    role: str
    company: str
    location: str = "New York, NY"
    salary: int
    years_exp: int
    notes: str = ""


class NegotiationResponse(BaseModel):
    market_rate: str
    counter_range: str
    negotiation_script: str
    key_points: str
    raw: str
    similar_jds_found: int
    similar_profiles_found: int


@router.post("", response_model=NegotiationResponse, summary="Get AI salary negotiation coaching")
async def negotiate(offer: OfferInput):
    # Build query string from offer for semantic search
    query = (
        f"{offer.role} engineer {offer.years_exp} years experience "
        f"{offer.location} salary ${offer.salary:,} {offer.notes}"
    )
    query_embedding = embed(query)

    # Retrieve market comps from Supabase via pgvector
    similar_jds      = search_job_descriptions(query_embedding, limit=5)
    similar_profiles = search_candidate_profiles(query_embedding, limit=3)

    # Pass context to Claude for coaching
    coaching = get_negotiation_coaching(
        offer=offer.model_dump(),
        similar_jds=similar_jds,
        similar_profiles=similar_profiles,
    )

    return NegotiationResponse(
        **coaching,
        similar_jds_found=len(similar_jds),
        similar_profiles_found=len(similar_profiles),
    )


class FreeNegotiateInput(BaseModel):
    situation: str


class FreeNegotiationResponse(BaseModel):
    strategy: str
    script: str
    tactics: str


@router.post("/free", response_model=FreeNegotiationResponse, summary="Negotiate anything")
async def negotiate_free(body: FreeNegotiateInput):
    coaching = get_free_negotiation_coaching(situation=body.situation)
    return FreeNegotiationResponse(**coaching)
