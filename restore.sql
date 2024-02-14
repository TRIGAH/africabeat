SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;
SET default_tablespace = '';
SET default_table_access_method = heap;
CREATE TABLE public.fingerprints (
    hash bytea NOT NULL,
    song_id integer NOT NULL,
    "offset" integer NOT NULL,
    date_created timestamp without time zone DEFAULT now() NOT NULL,
    date_modified timestamp without time zone DEFAULT now() NOT NULL
);
CREATE TABLE public.songs (
    song_id integer NOT NULL,
    song_name character varying(250) NOT NULL,
    fingerprinted smallint DEFAULT 0,
    file_sha1 bytea,
    total_hashes integer DEFAULT 0 NOT NULL,
    date_created timestamp without time zone DEFAULT now() NOT NULL,
    date_modified timestamp without time zone DEFAULT now() NOT NULL
);
CREATE SEQUENCE public.songs_song_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.songs_song_id_seq OWNED BY public.songs.song_id;
ALTER TABLE ONLY public.songs ALTER COLUMN song_id SET DEFAULT nextval('public.songs_song_id_seq'::regclass);
SELECT pg_catalog.setval('public.songs_song_id_seq', 35, true);
ALTER TABLE ONLY public.songs
    ADD CONSTRAINT pk_songs_song_id PRIMARY KEY (song_id);
ALTER TABLE ONLY public.fingerprints
    ADD CONSTRAINT uq_fingerprints UNIQUE (song_id, "offset", hash);
CREATE INDEX ix_fingerprints_hash ON public.fingerprints USING hash (hash);
ALTER TABLE ONLY public.fingerprints
    ADD CONSTRAINT fk_fingerprints_song_id FOREIGN KEY (song_id) REFERENCES public.songs(song_id) ON DELETE CASCADE;

