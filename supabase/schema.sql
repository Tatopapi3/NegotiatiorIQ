-- Enable pgvector extension
create extension if not exists vector;

-- Job descriptions table
create table if not exists job_descriptions (
    id          uuid primary key default gen_random_uuid(),
    title       text not null,
    company     text not null,
    location    text not null default 'New York, NY',
    salary_min  integer,
    salary_max  integer,
    content     text not null,
    embedding   vector(1536),
    created_at  timestamptz default now()
);

-- Candidate profiles table
create table if not exists candidate_profiles (
    id              uuid primary key default gen_random_uuid(),
    name            text,
    title           text not null,
    years_exp       integer not null,
    skills          text[] default '{}',
    content         text not null,
    embedding       vector(1536),
    created_at      timestamptz default now()
);

-- Vector similarity search for job descriptions
create or replace function match_job_descriptions(
    query_embedding vector(1536),
    match_count     int default 5
)
returns table (
    id          uuid,
    title       text,
    company     text,
    location    text,
    salary_min  integer,
    salary_max  integer,
    content     text,
    similarity  float
)
language sql stable
as $$
    select
        id, title, company, location, salary_min, salary_max, content,
        1 - (embedding <=> query_embedding) as similarity
    from job_descriptions
    where embedding is not null
    order by embedding <=> query_embedding
    limit match_count;
$$;

-- Vector similarity search for candidate profiles
create or replace function match_candidate_profiles(
    query_embedding vector(1536),
    match_count     int default 3
)
returns table (
    id          uuid,
    name        text,
    title       text,
    years_exp   integer,
    skills      text[],
    content     text,
    similarity  float
)
language sql stable
as $$
    select
        id, name, title, years_exp, skills, content,
        1 - (embedding <=> query_embedding) as similarity
    from candidate_profiles
    where embedding is not null
    order by embedding <=> query_embedding
    limit match_count;
$$;

-- Indexes for fast similarity search
create index if not exists job_descriptions_embedding_idx
    on job_descriptions using ivfflat (embedding vector_cosine_ops)
    with (lists = 100);

create index if not exists candidate_profiles_embedding_idx
    on candidate_profiles using ivfflat (embedding vector_cosine_ops)
    with (lists = 100);
