-- Opening Playbook: reminder emails (supabase/functions/nudge). Run this after schema.sql, in the SQL editor.
-- Before running it, replace the two placeholders below:
--   <PROJECT>       your project ref, the part before .supabase.co in the project URL
--   <NUDGE_SECRET>  the same long random string you gave the function with `supabase secrets set NUDGE_SECRET=…`
-- It is safe to run more than once.

-- One row per email sent. Only the function (service role) reads and writes it: no policies, so signed-in players see nothing.
create table if not exists public.nudges (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users (id) on delete cascade,
  kind text not null,
  sent_at timestamptz not null default now()
);
create index if not exists nudges_user_sent on public.nudges (user_id, sent_at desc);
alter table public.nudges enable row level security;
revoke all on public.nudges from anon, authenticated;

-- Every hour, a little after the hour. The function itself decides who (if anyone) gets an email: only players with
-- reminders on, only in their early evening, never twice in a week.
create extension if not exists pg_cron;
create extension if not exists pg_net;
select cron.unschedule('playbook-nudge') where exists (select 1 from cron.job where jobname = 'playbook-nudge');
select cron.schedule('playbook-nudge', '7 * * * *', $$
  select net.http_post(
    url := 'https://<PROJECT>.supabase.co/functions/v1/nudge',
    headers := jsonb_build_object('content-type', 'application/json', 'x-nudge-secret', '<NUDGE_SECRET>'),
    body := '{}'::jsonb)
$$);
