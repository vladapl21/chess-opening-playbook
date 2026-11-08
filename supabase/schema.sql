-- Opening Playbook: accounts and saved progress.
-- Paste this whole file into the Supabase SQL editor (Project → SQL Editor → New query) and press Run.
-- It is safe to run more than once.

-- One row per player: names and settings the app shows. Filled in on sign-up by the trigger below.
create table if not exists public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  display_name text,
  chesscom_username text,
  lichess_username text,
  daily_goal_minutes int,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- One row per player: the whole progress object the app keeps (drill lines, puzzles, practice games, course steps).
create table if not exists public.progress (
  user_id uuid primary key references auth.users (id) on delete cascade,
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

-- Row-level security: every player can read and write only their own rows.
alter table public.profiles enable row level security;
alter table public.progress enable row level security;

drop policy if exists "Read own profile" on public.profiles;
drop policy if exists "Update own profile" on public.profiles;
drop policy if exists "Insert own profile" on public.profiles;
create policy "Read own profile" on public.profiles for select to authenticated using ((select auth.uid()) = id);
create policy "Update own profile" on public.profiles for update to authenticated using ((select auth.uid()) = id) with check ((select auth.uid()) = id);
create policy "Insert own profile" on public.profiles for insert to authenticated with check ((select auth.uid()) = id);

drop policy if exists "Read own progress" on public.progress;
drop policy if exists "Insert own progress" on public.progress;
drop policy if exists "Update own progress" on public.progress;
drop policy if exists "Delete own progress" on public.progress;
create policy "Read own progress" on public.progress for select to authenticated using ((select auth.uid()) = user_id);
create policy "Insert own progress" on public.progress for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "Update own progress" on public.progress for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "Delete own progress" on public.progress for delete to authenticated using ((select auth.uid()) = user_id);

-- The app talks to these tables through the Data API as the signed-in user. Visitors who aren't signed in get nothing.
grant select, insert, update on public.profiles to authenticated;
grant select, insert, update, delete on public.progress to authenticated;
revoke all on public.profiles from anon;
revoke all on public.progress from anon;

-- Keep updated_at honest.
create or replace function public.touch_updated_at() returns trigger
language plpgsql set search_path = '' as $$
begin
  new.updated_at := now();
  return new;
end;
$$;
drop trigger if exists profiles_touch on public.profiles;
create trigger profiles_touch before update on public.profiles for each row execute function public.touch_updated_at();
drop trigger if exists progress_touch on public.progress;
create trigger progress_touch before insert or update on public.progress for each row execute function public.touch_updated_at();

-- Create the profile row when someone signs up.
create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  insert into public.profiles (id, display_name)
  values (new.id, coalesce(new.raw_user_meta_data ->> 'display_name', split_part(new.email, '@', 1)))
  on conflict (id) do nothing;
  return new;
end;
$$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users for each row execute function public.handle_new_user();
