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

alter table sessions add column if not exists user_id uuid;

-- 1.2 Messages Table
create table if not exists messages (
    id uuid primary key default uuid_generate_v4(),
    session_id uuid references sessions(id) on delete cascade not null,
    role text not null, -- 'user', 'assistant', 'system'
    content text not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    meta_info jsonb 
);

alter table messages add column if not exists meta_info jsonb;

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
    meta_info jsonb,
    doc_count integer default 0,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

alter table deliverables add column if not exists meta_info jsonb;
alter table deliverables add column if not exists doc_count integer default 0;

-- 1.5 Deliverable Documents Table (multi-file output)
create table if not exists deliverable_documents (
    id uuid primary key default uuid_generate_v4(),
    session_id uuid references sessions(id) on delete cascade not null,
    file_name text not null,
    content text not null,
    doc_type text,
    sort_order integer default 0,
    meta_info jsonb,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

create index if not exists idx_analysis_states_session_updated on analysis_states(session_id, updated_at desc);
create index if not exists idx_deliverable_docs_session_order on deliverable_documents(session_id, sort_order);

-- 1.6 Admin Configs (Human-in-the-loop control plane)
create table if not exists admin_configs (
    id uuid primary key default uuid_generate_v4(),
    config_key text not null,
    content_text text not null,
    content_json jsonb,
    version integer default 1,
    updated_by text,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

create unique index if not exists idx_admin_configs_key_version on admin_configs(config_key, version);
create index if not exists idx_admin_configs_key_updated on admin_configs(config_key, updated_at desc);

-- ==========================================
-- 2. Security Policies (RLS)
-- ==========================================
-- We enable RLS but allow public access for simplicity in this demo phase.
-- In a real production app, you would restrict 'user_id' rows to only match auth.uid()

alter table sessions enable row level security;
alter table messages enable row level security;
alter table analysis_states enable row level security;
alter table deliverables enable row level security;
alter table deliverable_documents enable row level security;
alter table admin_configs enable row level security;

-- Allow everything for now (Demo Mode)
drop policy if exists "Public Access Sessions" on sessions;
drop policy if exists "Public Access Messages" on messages;
drop policy if exists "Public Access Analysis" on analysis_states;
drop policy if exists "Public Access Deliverables" on deliverables;
drop policy if exists "Public Access Deliverable Documents" on deliverable_documents;
drop policy if exists "Public Access Admin Configs" on admin_configs;

create policy "Public Access Sessions" on sessions for all using (true) with check (true);
create policy "Public Access Messages" on messages for all using (true) with check (true);
create policy "Public Access Analysis" on analysis_states for all using (true) with check (true);
create policy "Public Access Deliverables" on deliverables for all using (true) with check (true);
create policy "Public Access Deliverable Documents" on deliverable_documents for all using (true) with check (true);
create policy "Public Access Admin Configs" on admin_configs for all using (true) with check (true);
