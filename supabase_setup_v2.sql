-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- ==========================================
-- 1. Tables Setup
-- ==========================================

-- 1.1 Sessions Table
-- Now includes user_id (nullable) to support both Guests and Registered Users
create table if not exists sessions (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid, -- Null for Guest, UUID for Registered User (links to auth.users)
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    status text default 'In Progress', -- 'In Progress', 'Completed'
    conversation_summary text,         
    archived_count integer default 0   
);

-- 1.2 Messages Table
create table if not exists messages (
    id uuid primary key default uuid_generate_v4(),
    session_id uuid references sessions(id) on delete cascade not null,
    role text not null, -- 'user', 'assistant', 'system'
    content text not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    meta_info jsonb 
);

-- 1.3 Analysis States Table
create table if not exists analysis_states (
    id uuid primary key default uuid_generate_v4(),
    session_id uuid references sessions(id) on delete cascade not null,
    json_state jsonb not null default '{}'::jsonb,
    system_notice text,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 1.4 Deliverables Table
create table if not exists deliverables (
    id uuid primary key default uuid_generate_v4(),
    session_id uuid references sessions(id) on delete cascade not null,
    content text not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- ==========================================
-- 2. Security Policies (RLS)
-- ==========================================
-- We enable RLS but allow public access for simplicity in this demo phase.
-- In a real production app, you would restrict 'user_id' rows to only match auth.uid()

alter table sessions enable row level security;
alter table messages enable row level security;
alter table analysis_states enable row level security;
alter table deliverables enable row level security;

-- Allow everything for now (Demo Mode)
create policy "Public Access Sessions" on sessions for all using (true) with check (true);
create policy "Public Access Messages" on messages for all using (true) with check (true);
create policy "Public Access Analysis" on analysis_states for all using (true) with check (true);
create policy "Public Access Deliverables" on deliverables for all using (true) with check (true);
