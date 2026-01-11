-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- 1. Sessions Table (Stores conversation metadata)
create table if not exists sessions (
    id uuid primary key default uuid_generate_v4(),
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    status text default 'In Progress', -- 'In Progress', 'Completed'
    conversation_summary text,         -- Stores the running summary from SummaryAgent
    archived_count integer default 0   -- Tracks how many messages have been summarized
);

-- 2. Messages Table (Stores chat history)
create table if not exists messages (
    id uuid primary key default uuid_generate_v4(),
    session_id uuid references sessions(id) on delete cascade not null,
    role text not null, -- 'user', 'assistant', 'system'
    content text not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    meta_info jsonb -- Optional: token usage, model name, etc.
);

-- 3. Analysis States Table (Stores the JSON state from AnalystAgent)
create table if not exists analysis_states (
    id uuid primary key default uuid_generate_v4(),
    session_id uuid references sessions(id) on delete cascade not null,
    json_state jsonb not null default '{}'::jsonb,
    system_notice text,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 4. Deliverables Table (Stores final output from ArchitectAgent)
create table if not exists deliverables (
    id uuid primary key default uuid_generate_v4(),
    session_id uuid references sessions(id) on delete cascade not null,
    content text not null, -- The full markdown report
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Row Level Security (RLS) Policies
-- For simplicity in this demo, we enable public access. 
-- IN PRODUCTION: You should configure Authentication and set restrictive policies.

alter table sessions enable row level security;
alter table messages enable row level security;
alter table analysis_states enable row level security;
alter table deliverables enable row level security;

-- Policy: Allow anonymous access for demo purposes (READ/WRITE)
create policy "Public Access Sessions" on sessions for all using (true) with check (true);
create policy "Public Access Messages" on messages for all using (true) with check (true);
create policy "Public Access Analysis" on analysis_states for all using (true) with check (true);
create policy "Public Access Deliverables" on deliverables for all using (true) with check (true);
